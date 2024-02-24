package com.rag;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.DocumentParser;
import dev.langchain4j.data.document.loader.FileSystemDocumentLoader;
import dev.langchain4j.data.document.parser.apache.pdfbox.ApachePdfBoxDocumentParser;
import dev.langchain4j.data.document.parser.apache.poi.ApachePoiDocumentParser;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.document.DocumentSplitter;
import java.nio.file.Path;
import java.nio.file.Paths;
import dev.langchain4j.data.segment.TextSegment;

import java.util.ArrayList;
import java.util.List;
import java.io.IOException;
import java.nio.file.Files;

public class DocumentIngester {

    public List<TextSegment> loadSplitAndCleanText(String path) throws IOException {

        // load the document
        Document document = generalDocumentLoader(path);
        //System.out.println(document);

        // split the document
        List<TextSegment> segments = splitDocument(document);
        
        // clean the segments in place
        cleanSegments(segments);
        //System.out.println(segments);
        

        return segments;
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
    

    



    private Document generalDocumentLoader(String path) throws IOException {
        
        Path filePath = Paths.get(path);
        Document document = null;

        if (path.endsWith(".pdf")) {
            document = FileSystemDocumentLoader.loadDocument(filePath, new ApachePdfBoxDocumentParser());
        } else if (path.endsWith(".docx")) {
            document = FileSystemDocumentLoader.loadDocument(filePath, new ApachePoiDocumentParser());
        } else if (path.endsWith(".txt") || path.endsWith(".md")) {

            String content = new String(Files.readAllBytes(filePath));
            document = new Document(content);
            System.out.println(document);
        }

        return document;
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
