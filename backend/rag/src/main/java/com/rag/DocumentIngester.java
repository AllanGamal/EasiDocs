package com.rag;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.document.DocumentSplitter;
import java.nio.file.Paths;
import dev.langchain4j.data.segment.TextSegment;
import java.util.ArrayList;
import java.util.List;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import com.google.gson.reflect.TypeToken;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.nio.file.Path;
import java.lang.reflect.Type;

public class DocumentIngester {

    public void loadSplitAndCleanDocuments() throws IOException, InterruptedException {

        List<Document> documents = loadDocumentsFromJsonWithCleanup(); // load docs
        List<TextSegment> segments = splitAllDocuments(documents); // split docs
        cleanSegments(segments); // clean

        // convert to json
        String json = convertDocumentsToJson(segments);

        // Write JSON to file
        Path path = Paths.get("../documentsy.json");
        try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
            writer.write(json);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /*
     * Convert a list of TextSegments to a JSON string
     * returns a JSON string
     */
    private String convertDocumentsToJson(List<TextSegment> segments) {
        Gson gson = new Gson();
        JsonArray jsonArray = new JsonArray();

        for (TextSegment segment : segments) {
            JsonObject jsonObject = new JsonObject();
            jsonObject.addProperty("text", segment.text());

            JsonObject metaObject = new JsonObject();
            metaObject.addProperty("source", segment.metadata().get("source"));
            metaObject.addProperty("page", segment.metadata().get("page"));
            // index of the segment of segments
            int index = segments.indexOf(segment);

            metaObject.addProperty("id", segment.metadata().get("source") + index);
            
            
            
            

            jsonObject.add("metadata", metaObject);
            jsonArray.add(jsonObject);
        }

        return gson.toJson(jsonArray);
    }
   
    /*
     * Split a single document into segments
     * returns a list of TextSegments
     */
    private static List<TextSegment> splitDocument(Document document) {
        DocumentSplitter splitter = DocumentSplitters.recursive(
                850,
                170);

        List<TextSegment> segments = splitter.split(document);
        return segments;
    }

    /*
     * Split a list of documents into segments
     * returns a list of TextSegments
     */
    private static List<TextSegment> splitAllDocuments(List<Document> documents) {
        List<TextSegment> segments = new ArrayList<>();

        for (Document document : documents) {
            if (document == null) {
                continue;
            }
            List<TextSegment> documentSegments = splitDocument(document);
            segments.addAll(documentSegments);
        }

        return segments;
    }

    /*
     * Clean the content of a list of TextSegments
     * replaces tabs and newlines with spaces
     */
    private static void cleanSegments(List<TextSegment> segments) {
        List<TextSegment> cleanedSegments = new ArrayList<>();
        for (TextSegment segment : segments) {
            String cleanedContent = segment.text().replaceAll("\t", " ").replaceAll("\n", " ");
            TextSegment cleanedSegment = new TextSegment(cleanedContent, segment.metadata()); 
                                                                                              
            cleanedSegments.add(cleanedSegment);
        }
        // clear segments and add the cleaned segments
        segments.clear();
        segments.addAll(cleanedSegments);
    }

   
    /*
     * Load a list of documents from a JSON file and remove the file
     * returns a list of Document objects
     */
    public static List<Document> loadDocumentsFromJsonWithCleanup() throws IOException {
        
        String filePath = "../documents.json";

        String jsonInput = new String(Files.readAllBytes(Paths.get(filePath)));
        List<Document> documents = null;
        
        // Create a Gson object with a my deserializer
        Gson gson = new GsonBuilder()
                .registerTypeAdapter(Document.class, new DocumentDeserializer()).create();

        Type listType = new TypeToken<List<Document>>() {
        }.getType();
        System.out.println(listType);

        try {
            documents = gson.fromJson(jsonInput, listType);
        } catch (Exception e) {
            e.printStackTrace();
        }

        // remove the file
        Files.delete(Paths.get(filePath));
        
        return documents;
    }

    

}
