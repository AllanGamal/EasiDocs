package com.rag;

import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {

        // make an object of the class
        DocumentIngester documentIngester = new DocumentIngester();

        documentIngester.loadSplitAndCleanText("/Users/allangamal/Documents/GitHub/EasiDocs/test.txt");



        System.out.println("Hello world!");
    }
}