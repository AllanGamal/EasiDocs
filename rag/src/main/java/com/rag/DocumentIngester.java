package com.rag;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.document.DocumentSplitter;
import java.nio.file.Paths;
import dev.langchain4j.data.segment.TextSegment;
import java.util.ArrayList;
import java.util.List;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import com.google.gson.reflect.TypeToken;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.nio.file.Path;
import java.lang.reflect.Type;

public class DocumentIngester {

    public List<TextSegment> loadSplitAndCleanDocuments() throws IOException, InterruptedException {
        


        List<Document> documents = loadDocumentsFromJsonWithCleanup();
        
        List<TextSegment> segments = splitAllDocuments(documents);
        cleanSegments(segments);
        // Start JSON construction here, after cleaning
        Gson gson = new Gson();
        String json = "[";

        int segmentSize = segments.size();

        for (int i = 0; i < segmentSize; i++) {
            TextSegment segment = segments.get(i);
            String source = segment.metadata().get("source"); // Assuming TextSegment also has getMetadata()
            String page = segment.metadata().get("page");

            String metastring = "\"metadata\": {\"source\": " + gson.toJson(source) + ", \"page\": " + gson.toJson(page)
                    + "}";

            json += "{" + "\"text\": " + gson.toJson(segment.text()) + ", " + metastring + "}";

            if (i < segmentSize - 1) {
                json += ", ";
            }
        }

        json += "]";
        System.out.println("test -----------------");

        // Write JSON to file
        Path path = Paths.get("../documentsy.json");
        Files.write(path, json.getBytes(StandardCharsets.UTF_8));
        // wait for the file to be written

        return segments;
    }

    private static List<TextSegment> splitDocument(Document document) {
        DocumentSplitter splitter = DocumentSplitters.recursive(
                850,
                170);

        List<TextSegment> segments = splitter.split(document);
        return segments;
    }

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

    private static void cleanSegments(List<TextSegment> segments) {
        List<TextSegment> cleanedSegments = new ArrayList<>();
        for (TextSegment segment : segments) {
            String cleanedContent = segment.text().replaceAll("\t", " ").replaceAll("\n", " ");
            TextSegment cleanedSegment = new TextSegment(cleanedContent, segment.metadata()); // create new segment with
                                                                                              // cleaned content
            cleanedSegments.add(cleanedSegment);
        }
        // clear segments and add the cleaned segments
        segments.clear();
        segments.addAll(cleanedSegments);
    }

    

    // [ Document { text = "ings of SID" metadata = {source=pdf/test.pdf, page=4} },
    // Document { text = "This is a test" metadata = {source=pdf/test.pdf, page=5}
    // }]

    public static List<Document> loadDocumentsFromJsonWithCleanup() throws IOException {
        // Läs innehållet från filen till en sträng
        // file path

        String filePath = "../documents.json";
        
        String jsonInput = new String(Files.readAllBytes(Paths.get(filePath)));
        List<Document> documents = null;
        // Använd Gson för att deserialisera JSON-strängen till Document-objekt
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
        
        // Ta bort JSON-filen efter deserialisering
        Files.delete(Paths.get(filePath));
        // Returnera listan av deserialiserade dokument
        return documents;
    }

    // main

}
