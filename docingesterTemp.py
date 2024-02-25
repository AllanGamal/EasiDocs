import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import TextLoader
import json

# supports .docx, .doc, .pdf, .txt, .md
def load_document(file):
    new_documents = []
    if file.endswith(".docx") or file.endswith(".doc"):
        new_documents = UnstructuredWordDocumentLoader(file).load()
    elif file.endswith(".pdf"):
        new_documents = PyPDFLoader(file).load()
    elif file.endswith(".txt") or file.endswith(".md"):
        new_documents = TextLoader(file).load()

    # skapa JSON från de nya dokumenten
    new_data = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in new_documents]


    # Kontrollera om filen redan finns
    if os.path.exists('documents.json'):
        # Om filen finns, läs den befintliga datan
        with open('documents.json', 'r') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:  # Hanterar tomma eller korrupta filer
                existing_data = []
    else:
        existing_data = []

    # Kombinera befintlig data med ny data
    combined_data = existing_data + new_data

    # Skriv den kombinerade datan till filen
    with open('documents.json', 'w') as json_file:
        json.dump(combined_data, json_file, indent=4)

load_document("pdf/test.pdf")





def load_document_batch(files):
    documents = []
    for file in files:
        documents.append(load_document(file))
    return documents
    
    return ValueError("File type not supported")
