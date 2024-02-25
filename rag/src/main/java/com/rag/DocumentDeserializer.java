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
        JsonObject meta = jsonObject.getAsJsonObject("metadata");
        Metadata metadata = new Metadata();

        for (Map.Entry<String, JsonElement> entry : meta.entrySet()) {
            // Antag att Metadata-klassen har en metod för att lägga till nya nyckel-värdepar.
            metadata.add(entry.getKey(), entry.getValue().getAsString());
        }

        // Antag att du har en lämplig konstruktor eller metod för att sätta dessa fält
        Document doc = new Document(pageContent, metadata);
        return doc;
    }
}
