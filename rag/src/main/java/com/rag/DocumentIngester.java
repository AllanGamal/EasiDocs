package com.rag;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.loader.FileSystemDocumentLoader;
import dev.langchain4j.data.document.parser.apache.pdfbox.ApachePdfBoxDocumentParser;
import dev.langchain4j.data.document.parser.apache.poi.ApachePoiDocumentParser;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.document.DocumentSplitter;
import dev.langchain4j.data.document.Metadata;

import java.nio.file.Path;
import java.nio.file.Paths;
import dev.langchain4j.data.segment.TextSegment;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import java.io.IOException;
import java.nio.file.Files;
import com.google.gson.reflect.TypeToken;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.lang.reflect.Type;

public class DocumentIngester {

    public List<TextSegment> loadSplitAndCleanText(String path) throws IOException {


        List<Document> documents = new ArrayList<>();

        // load the document
        Document document = generalDocumentLoader(path);
        //System.out.println(document);

        // split the document
        List<TextSegment> segments = splitDocument(document);
        
        // clean the segments in place
        cleanSegments(segments);

        return segments;
    }

    public List<TextSegment> loadSplitAndCleanTextFromFolder(String folderPath) throws IOException {
        List<TextSegment> allSegments = new ArrayList<>();
        
        Path startPath = Paths.get(folderPath);

        try (Stream<Path> stream = Files.walk(startPath)) {
            List<Path> filePaths = stream
                .filter(Files::isRegularFile)
                .filter(path -> path.toString().endsWith(".pdf") || 
                path.toString().endsWith(".docx") || 
                path.toString().endsWith(".txt") || 
                path.toString().endsWith(".md"))
                .collect(Collectors.toList()); // collect the paths into a list

            // load, split and clean each file
            for (Path filePath : filePaths) {
                List<TextSegment> segments = loadSplitAndCleanText(filePath.toString());
                allSegments.addAll(segments);
            }
        }


        for (TextSegment segment : allSegments) {
            System.out.println(segment);
        }



       
        
        return allSegments;
    }


    private void cleanSegments(List<TextSegment> segments) {
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
    

    



    private static Document generalDocumentLoader(String path) throws IOException {
        
        Path filePath = Paths.get(path);
        Document document = null;
        
        Metadata metadata = new Metadata();
        if (path.endsWith(".pdf")) {
            document = FileSystemDocumentLoader.loadDocument(filePath, new ApachePdfBoxDocumentParser());
        } else if (path.endsWith(".docx")) {
            document = FileSystemDocumentLoader.loadDocument(filePath, new ApachePoiDocumentParser());
        } else if (path.endsWith(".txt") || path.endsWith(".md")) {
            metadata.add("file_name", filePath.getFileName().toString());
            String content = new String(Files.readAllBytes(filePath));
            document = new Document(content, metadata);
            
        }
        
        return document;
    }

    public static List<Document> loadAndDeleteDocumentsFromJson(String filePath) throws IOException {
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


    
    
        public static void main(String[] args) throws InterruptedException {
            try {
                ProcessBuilder pb = new ProcessBuilder("python3", "docingesterTemp.py");
                Process p = pb.start();
                int exitCode = p.waitFor();
                List<Document> documents = loadAndDeleteDocumentsFromJson("documents.json");
                if (exitCode != 0) {
                    throw new RuntimeException("Python script exited with error code: " + exitCode);
                }
                System.out.println(documents);
                // print type of documents
                System.out.println(documents.get(0).getClass());
               

    
                // Nu kan du använda 'documents'-listan som innehåller dina deserialiserade Document-objekt
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    


    private List<TextSegment> splitDocument(Document document) {
        DocumentSplitter splitter = DocumentSplitters.recursive(
                850,
                170);

        List<TextSegment> segments = splitter.split(document);
        return segments;
    }

    // main

}
