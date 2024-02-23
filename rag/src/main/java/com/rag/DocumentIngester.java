package com.rag;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.DocumentParser;
import dev.langchain4j.data.document.loader.FileSystemDocumentLoader;
import dev.langchain4j.data.document.parser.apache.pdfbox.ApachePdfBoxDocumentParser;
import dev.langchain4j.data.document.parser.apache.pdfbox.ApachePdfBoxDocumentParser;
import dev.langchain4j.data.document.parser.apache.poi.ApachePoiDocumentParser;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.document.DocumentSplitter;
import java.nio.file.Path;
import java.nio.file.Paths;
import dev.langchain4j.data.segment.TextSegment;
import java.util.List;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class DocumentIngester {

    public String ingestDocument(String path) throws IOException {

        // if the file is a pdf
        Path filePath = Paths.get(path);
        Document document = null;

        if (path.endsWith(".pdf")) {
            document = FileSystemDocumentLoader.loadDocument(filePath, new ApachePdfBoxDocumentParser());
        } else if (path.endsWith(".docx")) {
            document = FileSystemDocumentLoader.loadDocument(filePath, new ApachePoiDocumentParser());
        } else if (path.endsWith(".txt") || path.endsWith(".md")) {

            String content = new String(Files.readAllBytes(filePath));
            String normalizedContent = content.replaceAll("\r\n", "\n").replaceAll("\r", "\n");

            document = new Document(normalizedContent);
        }

        document = cleanDocument(document);
        DocumentSplitter splitter = DocumentSplitters.recursive(
                2112,
                100);

        List<TextSegment> segments = splitter.split(document);
        // System.out.println(segments);

        for (TextSegment segment : segments) {
            System.out.println(segment);

        }

        return document.toString();
    }

    public Document cleanDocument(Document document) {
        // remove all the next row (\n) and tabs (\t)
        String dirtyText = document.text();

        String cleanedText = dirtyText.replaceAll("\t", " ").replaceAll("\n", " ");

        Document cleanedDocument = new Document(cleanedText, document.metadata());

        return cleanedDocument;

    }

    // main

}
