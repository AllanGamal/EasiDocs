import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import TextLoader
import json
from prompt_template import prompt as prompt
import os.path,subprocess
from subprocess import STDOUT,PIPE
from sys import stdin


# supports .docx, .doc, .pdf, .txt, .md
def load_document(file):
    
    new_documents = []
    if (file.endswith(".docx") | file.endswith(".doc")):
        new_documents =  UnstructuredWordDocumentLoader(file).load()
    if (file.endswith(".pdf")):
        new_documents = (PyPDFLoader(file).load())
    if (file.endswith(".txt") | file.endswith(".md")):
        new_documents =  TextLoader(file).load()
    
    filename = os.path.basename(file)
    print("Loading filename: " + filename)

    # add filename to metadata
    for doc in new_documents:
        doc.metadata['source'] = filename

    # skapa JSON från de nya dokumenten
    new_data = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in new_documents]
    
    

    # om fil redan finns
    if os.path.exists('../../backend/documents.json'):
        # lägg till data till bifintlig fil
        with open('../../backend/documents.json', 'r') as json_file:
            try:
                existing_data = json.load(json_file) 
            except json.JSONDecodeError:  # hanterar  korrupta filer
                existing_data = [] 
    else:
        existing_data = [] # om filen inte finns, skapa en tom lista

    # Kombinera befintlig data med ny data
    combined_data = existing_data + new_data

    # Skriv den kombinerade datan till filen
    with open('../../backend/documents.json', 'w') as json_file:
        json.dump(combined_data, json_file, indent=4)
    
    return new_documents



def load_document_batch(files):
    
    documents = []
    for file in files:
        documents.append(load_document(file))
    return documents
   
    










