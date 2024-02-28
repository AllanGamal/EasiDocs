package com.rag;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.document.DocumentSplitter;
import java.nio.file.Paths;
import dev.langchain4j.data.segment.TextSegment;
import java.util.ArrayList;
import java.util.List;
import java.io.IOException;
import java.nio.file.Files;
import com.google.gson.reflect.TypeToken;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.nio.file.Path;
import java.lang.reflect.Type;

public class DocumentIngester {

    public List<TextSegment> loadSplitAndCleanDocuments() throws IOException, InterruptedException {
        
        List<Document> documents = loadDocumentsFromPythonScript();
        List<TextSegment> segments = splitAllDocuments(documents);

        cleanSegments(segments);
        


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
            List<TextSegment> documentSegments = splitDocument(document);
            segments.addAll(documentSegments);
        }
        return segments;
    }


    private static void cleanSegments(List<TextSegment> segments) {
        List<TextSegment> cleanedSegments = new ArrayList<>();
        for (TextSegment segment : segments) {
            String cleanedContent = segment.text().replaceAll("\t", " ").replaceAll("\n", " ");
            TextSegment cleanedSegment = new TextSegment(cleanedContent, segment.metadata()); // create new segment with cleaned content
            cleanedSegments.add(cleanedSegment);
        }
        // clear segments and add the cleaned segments
        segments.clear();
        segments.addAll(cleanedSegments); 
    }

   

        private static List<Document> loadDocumentsFromPythonScript() throws InterruptedException {
            System.out.println("Loading documents from Python script...");
            try {
                
                
                List<Document> documents = loadDocumentsFromJsonWithCleanup("../documents.json");
                
                
                Gson gson = new Gson();
                String json = "";

                // put the text in the empty json file, with metadata (page and source) as objects
                for (Document document : documents) {
                    // get source 
                    String source = document.metadata().get("source");
                    // get page
                    String page = document.metadata().get("page");
                    String metastring = "metadata = {source=" + source + ", page=" + page + "}";
                    json = json + "{" + gson.toJson(document.text()) + ", " + metastring + "}";
                    // if not last document, add a comma
                    if (documents.indexOf(document) != documents.size() - 1) {
                        json = json + ", ";
                    }
                    

                }
                System.out.println(json);
                
                
                Path path = Paths.get("../documents.json");
                

                

                return documents;
                
                
                // Nu kan du använda 'documents'-listan som innehåller dina deserialiserade Document-objekt
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
        
        
        //[ Document { text = "ings of SID" metadata = {source=pdf/test.pdf, page=4} }, Document { text = "This is a test" metadata = {source=pdf/test.pdf, page=5} }]

   

    public static List<Document> loadDocumentsFromJsonWithCleanup(String filePath) throws IOException {
        // Läs innehållet från filen till en sträng
        String jsonInput = new String(Files.readAllBytes(Paths.get(filePath)));
        
        

        // Använd Gson för att deserialisera JSON-strängen till Document-objekt
        Gson gson = new GsonBuilder()
                .registerTypeAdapter(Document.class, new DocumentDeserializer()) // Antag att du har en anpassad deserialiserare
                .create();
        
        
        Type listType = new TypeToken<List<Document>>(){}.getType();
        List<Document> documents = gson.fromJson(jsonInput, listType);
        
        
        
        // Ta bort JSON-filen efter deserialisering
        Files.delete(Paths.get(filePath));
        

        // Returnera listan av deserialiserade dokument
        return documents;
    }


    // main

}
