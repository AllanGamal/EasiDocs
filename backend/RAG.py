from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from prompt_template import prompt as prompt
import os.path
from subprocess import STDOUT,PIPE
from sys import stdin
import subprocess
from docingesterTemp import load_document_batch
import json
from langchain.docstore.document import Document




#document = document_ingestion.load_document("ark.pdf")
#documents = load_document_batch(["test.pdf", "test.docx", "test.txt"])
# load all documents in a folder

#documents = document_ingestion.load_documents_from_folder("pdf")
# define the documents

# stop the timer

def runItAll(query):
    print("running")

    # save in chromadb folder
    vector_dir = "/Users/allangamal/Documents/GitHub/EasiDocs/backend/chromadb"

    import time
    # initialize the vector store/db
    embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
    db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder

    retriever = db.as_retriever(search_kwargs={"k": 3}) # k=3 => 3 sources
    db = 1
    embedding_function = 1
    llm = Ollama(model="mistral")
    
    start = time.time()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", 
        retriever=retriever, # 3 sources
        return_source_documents=True,
        
    )
    query2_en = "Have AR or VR revealed any potential in the education sector?"
    result = qa.invoke(query)

    answer = result["result"]
    sources = result["source_documents"]
    end = time.time()
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("Time elapsed: ", end - start)
    print("ANSWER")
    print(answer)
    print("SOURCES")
    for source in sources:
        print(source)
    
    return answer
