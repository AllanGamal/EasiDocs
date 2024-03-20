use actix_cors::Cors;
use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::Deserialize;
use std::fs;
use pyo3::prelude::*;
use std::path::Path;


#[derive(Deserialize)]
struct Message {
    message: String,
    is_english: bool,
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
    println!("Received query: {}", message.message);
    println!("Language: {}", message.is_english);
    let query = message.message.clone();
    let is_english = message.is_english;

    match execute_rag_query(query, is_english).await {
        Ok((answer, metadata)) => {
            HttpResponse::Ok().json(serde_json::json!({ "answer": answer, "metadata": metadata }))
        }
        Err(e) => {
            eprintln!("Failed to execute Python function: {:?}", e);
            HttpResponse::InternalServerError().body(format!("Failed to execute Python function: {:?}", e))
        }
    }
}

async fn execute_rag_query(query: String, is_english: bool) -> PyResult<(String, Vec<String>)> {
    Python::with_gil(|py| {
        let sys = PyModule::import(py, "sys").unwrap();
        sys.getattr("path").unwrap().call_method1("append", ("../../backend",)).unwrap();
        
        let python_script = PyModule::import(py, "RAG")?;
        let (answer, metadata): (String, Vec<String>) = python_script.call_method1("get_rag_response", (&query, is_english))?.extract()?;
        Ok((answer, metadata))
    })
}


async fn load_documents_to_db(paths: Vec<String>) -> PyResult<()> {
    Python::with_gil(|py| {
        let sys = PyModule::import(py, "sys")?;
        sys.getattr("path")?.call_method1("append", ("../../backend",))?;
        
        let python_script = PyModule::import(py, "RAG")?;

        // Convert the Rust Vec<String> to Python list
        let py_paths = paths.into_py(py);

        // Call the Python function without extracting the return value
        python_script.call_method1("load_documents_to_db", (py_paths,))?;

        Ok(())
    })
}


async fn handle_file_paths(paths: web::Json<FilePaths>) -> impl Responder {
    let documents_store_dir = "../../backend/pdf";
    println!("Received file paths: {:?}", paths.file_paths);

    let mut successful_copies = Vec::new();

    for path in &paths.file_paths {
        let file_name = Path::new(path).file_name().unwrap();
        let destination = format!("{}/{}", documents_store_dir, file_name.to_str().unwrap());

        if !Path::new(&destination).exists() {
            match fs::copy(path, &destination) {
                Ok(_) => {
                    println!("Successfully copied {} to {}", path, destination);
                    successful_copies.push(destination);
                },
                Err(e) => eprintln!("Failed to copy {} to {}: {}", path, destination, e),
            }
        } else {
            println!("File {} already exists in {}", file_name.to_str().unwrap(), documents_store_dir);
        }
    }

    if !successful_copies.is_empty() { 
        match load_documents_to_db(successful_copies.clone()).await {
            Ok(_) => println!("Successfully loaded documents to the database: {:?}", successful_copies),
            Err(e) => eprintln!("Failed to load documents to the database: {:?}", e),
        }
    }

    HttpResponse::Ok().body("File paths received and files processed")
}




async fn load_file_list() -> HttpResponse {
    let uploads_dir = "../../backend/pdf";
    

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

            // Proceed to delete the associated document from the database
            match delete_doc_from_database(file_path.file_path.clone()).await {
                Ok(_) => {
                    // print Document deletion from database was successful with file path
                    println!("Document deletion from database was successful with file path: {:?}", file_path.file_path);
                    println!("");
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