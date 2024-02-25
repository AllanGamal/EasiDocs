from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import TextLoader
import json




# supports .docx, .doc, .pdf, .txt, .md
def load_document(file):
    if (file.endswith(".docx") | file.endswith(".doc")):
        return UnstructuredWordDocumentLoader(file).load()
    if (file.endswith(".pdf")):
        
        return PyPDFLoader(file).load()
    if (file.endswith(".txt") | file.endswith(".md")):
        return TextLoader(file).load()
    
    return ValueError("File type not supported")




def load_document_batchy(files):
    print(files)
    documents = []
    for file in files:
        documents.append(load_document(file))
    print(documents)
    return documents
load_document_batchy(["pdf/test.pdf"])


#takes the text and splits it into chunks.
def split_document(document, chunk_size=800, chunk_overlap=160): # 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = text_splitter.split_documents(document)
    return docs

def split_document_batch(documents):
    docs = []
    for doc in documents:
        chunks = split_document(doc)  # returns a list of Document objects
        for chunk in chunks:  # adds each chunk to the list of documents
            docs.append(chunk)
    return docs


def clean_documents(docs):
    for doc in docs:
        doc.page_content = doc.page_content.replace("\n", " ").replace("\t", " ")

def get_page_contents(docs):
    page_contents = []
    for doc in docs:
        page_contents.append(doc.page_content)
    return page_contents