from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from LocalLLM import LocalLLM
from langchain_community.document_loaders import PyPDFLoader
import chromadb
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import Docx2txtLoader
# import
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader





# initializing the embeddings



llm = Ollama(model="mistral")

def load_pdf(file):
    loader = PyPDFLoader(file)
    documents = loader.load()
    return documents

def load_document(file):
    if (file.endswith(".docx") | file.endswith(".doc")):
        return UnstructuredWordDocumentLoader(file, mode="single").load()
    if (file.endswith(".pdf")):
        return PyPDFLoader(file).load()
    if (file.endswith(".txt") | file.endswith(".md")):
        return TextLoader(file).load()
    
    return ValueError("File type not supported")



document = load_document("test.md")


#takes the text and splits it into chunks.
def split_document(document, chunk_size=650, chunk_overlap=150): # 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = text_splitter.split_documents(document)
    return docs


docs = split_document(document)


def clean_documents(docs):
    for doc in docs:
        doc.page_content = doc.page_content.replace("\n", " ").replace("\t", " ")
    

clean_documents(docs)

def get_page_contents(docs):
    page_contents = []
    for doc in docs:
        page_contents.append(doc.page_content)
    return page_contents

page_contents = get_page_contents(docs)

chroma_client = chromadb.Client()

embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")


def init_database(docs, embedding_function):
    db = Chroma.from_documents(
        docs,
        embedding_function,
    )
    return db

db = init_database(docs, embedding_function)


def search_database(db, query, k=3):
    return db.similarity_search(query, k)


print("2")

query = "What kind of technologies are reshaping education systems? "
query_sv = "Vilka teknologier omformar utbildningssystemen?"
docs = db.similarity_search(query, k=3)
docs_sv = db.similarity_search(query_sv, k=3)
print("")
print("")
print("")
print(docs[0])
print("---------------------------------------------------------------------------------------------------------------------------------")
print(docs[1])
print("---------------------------------------------------------------------------------------------------------------------------------")
print("")
print("---------------------------------------------------------------------------------------------------------------------------------")
print(docs_sv[0])
print("---------------------------------------------------------------------------------------------------------------------------------")
print(docs_sv[1])



