package com.rag;

import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.Metadata;


import com.google.gson.JsonDeserializationContext;

import java.lang.reflect.Type;
import java.util.Map;

class DocumentDeserializer implements JsonDeserializer<Document> {
    @Override
    public Document deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
        JsonObject jsonObject = json.getAsJsonObject();
        
        

        // Hämta page_content
        String pageContent = jsonObject.get("page_content").getAsString();
       

        System.out.println("-----------------");

        // Hämta metadata-objektet
        JsonObject metaObject = jsonObject.getAsJsonObject("metadata");
        

        // Skapa ett nytt Metadata-objekt
        Metadata metadata = new Metadata();

        // Iterera över varje entry i metadata JSON-objektet och lägg till page och sour
        String source = metaObject.get("source").getAsString();
        String page = metaObject.get("page").getAsString();
        for (Map.Entry<String, JsonElement> entry : metaObject.entrySet()) {
            metadata.add(entry.getKey(), entry.getValue().getAsString());
        }

        // Skapa och returnera ett nytt Document-objekt med insamlad data
        Document document = new Document(pageContent, metadata);

        // Skriv ut source och page från metadata
    System.out.println("Source: " + metaObject.get("source").getAsString());
    System.out.println("Page: " + metaObject.get("page").getAsString());
        

        return document;
    }

    

    
}