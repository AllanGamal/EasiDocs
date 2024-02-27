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
        
        String pageContent = jsonObject.get("page_content").getAsString();
        
        System.out.println("-----------------");

        JsonObject metaObject = jsonObject.getAsJsonObject("metadata");
        Metadata metadata = new Metadata();
        for (Map.Entry<String, JsonElement> entry : metaObject.entrySet()) {
            metadata.add(entry.getKey(), entry.getValue().getAsString());
        }
        
        

        return new Document(pageContent, metadata);
    }
}

