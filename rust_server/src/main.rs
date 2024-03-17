use actix_cors::Cors;
use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::Deserialize;
use std::fs;
use pyo3::prelude::*;
use std::path::Path;


#[derive(Deserialize)]
struct Message {
    message: String,
}
#[derive(Deserialize)]
struct FilePaths {
    file_paths: Vec<String>,
}

#[derive(Deserialize)]
struct FilePath {
    file_path: String,
}

async fn handle_message(message: web::Json<Message>) -> impl Responder {
    println!("Received message: {}", message.message);
    let query = message.message.clone();

   
    match execute_rag_query(query).await {
        Ok(result) => {
            println!("Result: {}", result);
            HttpResponse::Ok().body(result) 
        }
        Err(e) => {
            eprintln!("Failed to execute Python function: {:?}", e);
            HttpResponse::InternalServerError().body(format!("Failed to execute Python function: {:?}", e))
        }
    }
}

async fn execute_rag_query(query: String) -> PyResult<String> {
    Python::with_gil(|py| {
        let sys = PyModule::import(py, "sys").unwrap();
        sys.getattr("path").unwrap().call_method1("append", ("../../backend",)).unwrap();
        
        let python_script = PyModule::import(py, "RAG")?;
        let result: String = python_script.call_method1("get_rag_response", (&query,))?.extract()?;
        println!("Python function returned: {}", result);
        Ok(result)
    })
}



async fn handle_file_paths(paths: web::Json<FilePaths>) -> impl Responder {
    let documents_store_dir = "../../backend/pdf";

    println!("Received file paths: {:?}", paths.file_paths);

    for path in &paths.file_paths {
        let file_name = Path::new(path).file_name().unwrap();
        let destination = format!("{}/{}", documents_store_dir, file_name.to_str().unwrap());

        // copy the file if it does not already exist in dir
        if !Path::new(&destination).exists() {
            match fs::copy(path, &destination) {
                Ok(_) => println!("Successfully copied {} to {}", path, destination),
                Err(e) => eprintln!("Failed to copy {} to {}: {}", path, destination, e),
            }
        } else {
            println!("File {} already exists in {}", file_name.to_str().unwrap(), documents_store_dir);
        }
    }

    HttpResponse::Ok().body("File paths received and files copied")
}


async fn load_file_list() -> HttpResponse {
    let uploads_dir = "../../backend/pdf";
    println!("Reading files from: {}", uploads_dir);

    // read the directory's contents
    match fs::read_dir(uploads_dir) {
        Ok(entries) => {
            // collect file names
            let file_names: Vec<String> = entries.filter_map(|entry| {
                entry.ok().and_then(|e| {
                    let path = e.path();
                    if path.is_file() && matches!(path.extension().and_then(|s| s.to_str()), Some("pdf" | "docx" | "doc" | "txt" | "md")) {
                        path.file_name().and_then(|n| n.to_str()).map(String::from)
                    } else {
                        None
                    }
                })
            }).collect();
            println!("Files: {:?}", file_names);
            HttpResponse::Ok().json(file_names) // list of files as a JSON response
        },
        Err(e) => {
            eprintln!("Failed to read the uploads directory: {}", e);
            HttpResponse::InternalServerError().finish()
        }
    }
}


async fn delete_file(file_path: web::Json<FilePath>) -> HttpResponse {
    // file path construction
    let base_path = "../../backend/";
    let full_path = base_path.to_owned() + &file_path.file_path;

    // delete the file from the filesystem
    match fs::remove_file(&full_path) {
        Ok(_) => {
            println!("File deleted: {:?}", full_path);

            // Proceed to delete the associated document from the database
            match delete_doc_from_database(file_path.file_path.clone()).await {
                Ok(_) => {
                    println!("Document deletion from database was successful");
                    HttpResponse::Ok().finish()
                },
                Err(e) => {
                    eprintln!("Failed to delete document from database: {:?}", e);
                    HttpResponse::InternalServerError().finish()
                }
            }
        },
        Err(e) => {
            eprintln!("Failed to delete file {:?}: {}", full_path, e);
            HttpResponse::InternalServerError().finish()
        },
    }
}
// path = string
async fn delete_doc_from_database(path: String) -> PyResult<()> {
    Python::with_gil(|py| {
        let sys = PyModule::import(py, "sys")?;
        sys.getattr("path")?.call_method1("append", ("../../backend",))?;
        
        let python_script = PyModule::import(py, "databaseManager")?;
        
        // Pass path directly as a string, not as part of a tuple
        python_script.call_method1("deleteDocumentsBySourceFromDb", (path,))?;

        Ok(())
    })
}



#[actix_web::main]
async fn main() -> std::io::Result<()> {
    
    HttpServer::new(|| { // create a new server
        let cors = Cors::permissive(); 

        App::new() // create a new application
            .wrap(cors) // wrap the application with  cors middleware
            .service( // sets up a route for application,
                web::resource("/message") // post request to /message,  
                    .route(web::post().to(handle_message)) // => handle_message called
            )
            .service(
                // Set up a route for handling file uploads.
                web::resource("/upload")
                    .route(web::post().to(handle_file_paths)),
            ).service(
                // Set up a route for handling file uploads.
                web::resource("/files")
                    .route(web::get().to(load_file_list)),
            ).service(
                // Set up a route for handling file uploads.
                web::resource("/delete")
                    .route(web::delete().to(delete_file)),
            )
    })
    .bind("127.0.0.1:8001")?
    .run()
    .await
}