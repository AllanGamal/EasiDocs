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
        
        // Check if pageContent is null or blank
        
        if (pageContent == null || pageContent.isBlank()) {
            return null;
        }
        
       
        // Hämta metadata-objektet
        JsonObject metaObject = jsonObject.getAsJsonObject("metadata");
        
        // Skapa ett nytt Metadata-objekt
        Metadata metadata = new Metadata();

        for (Map.Entry<String, JsonElement> entry : metaObject.entrySet()) {
            metadata.add(entry.getKey(), entry.getValue().getAsString());
        }

        // Skapa och returnera ett nytt Document-objekt med insamlad data
        Document document = new Document(pageContent, metadata);

        return document;
    }
}