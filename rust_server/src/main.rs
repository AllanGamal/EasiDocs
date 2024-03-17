use actix_cors::Cors;
use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::Deserialize;
use std::fs;
use pyo3::prelude::*;


#[derive(Deserialize)]
struct Message {
    message: String,
}
#[derive(Deserialize)]
struct FilePaths {
    file_paths: Vec<String>,
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
    println!("Received file paths: {:?}", paths.file_paths);
    HttpResponse::Ok().body("File paths received")
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






#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();
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
            )
    })
    .bind("127.0.0.1:8001")?
    .run()
    .await
}