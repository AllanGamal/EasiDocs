use actix_cors::Cors;
use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::Deserialize;
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
    // strng k
    let _ = call_python_function().await;
    
    
    HttpResponse::Ok().body("Message received")
}

async fn handle_file_paths(paths: web::Json<FilePaths>) -> impl Responder {
    println!("Received file paths: {:?}", paths.file_paths);
    HttpResponse::Ok().body("File paths received")
}

async fn call_python_function() -> PyResult<()> {
    Python::with_gil(|py| {
        let sys = PyModule::import(py, "sys").unwrap();
        sys.getattr("path").unwrap().call_method1("append", ("/Users/allangamal/Documents/GitHub/EasiDocs/backend",)).unwrap();
        
        let python_script = PyModule::import(py, "RAG")?;
        
        
        let result: String = python_script.call_method1("runItAll", ("Have AR or VR revealed any potential in the education sector?",))?.extract()?;

        println!("Python function returned: {}", result);
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
            )
    })
    .bind("127.0.0.1:8001")?
    .run()
    .await
}