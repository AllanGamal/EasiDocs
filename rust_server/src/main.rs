use actix_cors::Cors;
use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::Deserialize;

#[derive(Deserialize)]
struct Message {
    message: String,
}

async fn handle_message(message: web::Json<Message>) -> impl Responder {
    println!("Received message: {}", message.message);
    HttpResponse::Ok().body("Message received")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| { // create a new server
        let cors = Cors::permissive(); 

        App::new() // create a new application
            .wrap(cors) // wrap the application with the cors middleware
            .service( // sets up a route for the application,
                web::resource("/message") // post request to /message,  
                    .route(web::post().to(handle_message)) // => handle_message called
            )
    })
    .bind("127.0.0.1:8000")?
    .run()
    .await
}
