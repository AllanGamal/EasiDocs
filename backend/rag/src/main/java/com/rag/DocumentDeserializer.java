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
    /*
     * Deserialize a JSON object to a Document object
     * returns a Document object
     */
    @Override
    public Document deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
        JsonObject jsonObject = json.getAsJsonObject();
        
        // get pageContent
        String pageContent = jsonObject.get("page_content").getAsString();
        
        // Check if pageContent is null or blank
        if (pageContent == null || pageContent.isBlank()) {
            return null;
        }
        
        // get metadata
        JsonObject metaObject = jsonObject.getAsJsonObject("metadata");
        
        // create a new Metadata object
        Metadata metadata = new Metadata();

        // loop through metadata objects and add key-value pair to the metadata object
        for (Map.Entry<String, JsonElement> entry : metaObject.entrySet()) {
            metadata.add(entry.getKey(), entry.getValue().getAsString());
        }

        // create and return a new Document object with the pageContent and metadata
        Document document = new Document(pageContent, metadata);

        return document;
    }
}