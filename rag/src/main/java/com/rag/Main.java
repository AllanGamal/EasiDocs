package com.rag;

import java.io.IOException;
import java.util.List;


import dev.langchain4j.data.segment.TextSegment;

public class Main {
    public static void main(String[] args) throws IOException, InterruptedException {
        try {
            System.out.println("Hello world!");
            DocumentIngester documentIngester = new DocumentIngester();
            List<TextSegment> segments = documentIngester.loadSplitAndCleanDocuments();
            
        // make an object of the class

        // documentIngester.loadSplitAndCleanText("/Users/allangamal/Documents/GitHub/EasiDocs/test.md");
        // documentIngester.loadSplitAndCleanTextFromFolder("/Users/allangamal/Documents/GitHub/EasiDocs/testFolder");

        } catch (Exception e) {
            System.out.println("Hello world!");
        }
        
    }
}