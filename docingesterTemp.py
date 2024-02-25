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
    if file.endswith(".docx") or file.endswith(".doc"):
        new_documents = UnstructuredWordDocumentLoader(file).load()
    elif file.endswith(".pdf"):
        new_documents = PyPDFLoader(file).load()
    elif file.endswith(".txt") or file.endswith(".md"):
        new_documents = TextLoader(file).load()

    # skapa JSON från de nya dokumenten
    new_data = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in new_documents]


    # om fil redan finns
    if os.path.exists('documents.json'):
        # lägg till data till bifintlig fil
        with open('documents.json', 'r') as json_file:
            try:
                existing_data = json.load(json_file) 
            except json.JSONDecodeError:  # hanterar  korrupta filer
                existing_data = [] 
    else:
        existing_data = [] # om filen inte finns, skapa en tom lista

    # Kombinera befintlig data med ny data
    combined_data = existing_data + new_data

    # Skriv den kombinerade datan till filen
    with open('documents.json', 'w') as json_file:
        json.dump(combined_data, json_file, indent=4)



def load_document_batch(files):
    documents = []
    for file in files:
        documents.append(load_document(file))
    print(documents)
    return documents


def test(files):
    documents = load_document_batch(files)
    print(documents)
    command = ['mvn', 'exec:java', '-Dexec.mainClass=com.rag.Main']
    project_root = 'rag'

    # Kör Maven-kommandot
    # blocking process


    process = subprocess.Popen(command, cwd=project_root)
    process.wait()
    return documents


load_document_batch(["pdf/test.pdf"])



