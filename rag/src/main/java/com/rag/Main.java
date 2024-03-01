package com.rag;

import java.io.IOException;


public class Main {

    /*
     * Main method
     */
    public static void main(String[] args) throws IOException, InterruptedException {
        try {
            System.out.println("Hello world!");
            DocumentIngester documentIngester = new DocumentIngester();
            documentIngester.loadSplitAndCleanDocuments();
            
        } catch (Exception e) {
            System.out.println("Hello world!");
        }
        
    }
}