from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from prompt_template import prompt as prompty
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
'''
load_document_batch(["pdf/ark.pdf", "pdf/test.pdf", "pdf/22.pdf", "pdf/33.pdf",  "pdf/64.pdf","pdf/46.pdf", "pdf/180.pdf"])
load_document_batch(["pdf/ark.pdf", "pdf/test.pdf", "pdf/22.pdf", "pdf/33.pdf",  "pdf/64.pdf"])


# cocument splitting and cleaning (running java code)
def run_maven():
    command = ['mvn', 'exec:java', '-Dexec.mainClass=com.rag.Main']
    project_root = 'rag'
    process = subprocess.Popen(command, cwd=project_root)
    process.wait()
     
run_maven()

json_file_path = "documentsy.json"
print(json_file_path)
# Load and parse the JSON data from the file
with open(json_file_path, 'r') as json_file:
    documents_data = json.load(json_file)


print("Going through the documents")
# Create a list of Document objects
documents = [Document(page_content=doc.get('text'), metadata=doc.get('metadata')) for doc in documents_data]
           
# remove json
os.remove(json_file_path)
print("Removed json file")
# lägg till page_content och metadata från json



# save in chromadb folder
vector_dir = "chromadb/VectorStore"

import time
# initialize the vector store/db
embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
'''
'''
db = Chroma.from_documents(
        documents,
        embedding_function,
        persist_directory=vector_dir, # save in chromadb folder
    )



'''

def run_maven():
    project_root = '../../backend/rag' 
    print(f"\nRunning Maven in {project_root}")
    
    if not os.path.exists(os.path.join(project_root, 'pom.xml')):
        print("Error: pom.xml not found in the project root.")
        return
    
    command = ['mvn', 'exec:java', '-Dexec.mainClass=com.rag.Main']
    process = subprocess.Popen(command, cwd=project_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()  # This waits for the process to complete
    
    if process.returncode != 0:
        print(f"Maven execution failed:\n{stderr.decode()}")
    else:
        print(f"Maven executed successfully:\n" + "Java code executed successfully \n")
        print("Please wait for documents to be loaded to the db...\n")

def load_documents_to_db(file_paths_arr):
    print("Loading documents to db")
    project_root = '../../backend/'  
    load_document_batch(file_paths_arr)

    # cocument splitting and cleaning (running java code)
    run_maven()

    json_file_path = project_root + "documentsy.json"
    # load and parse  JSON data from file
    with open(json_file_path, 'r') as json_file:
        documents_data = json.load(json_file)

    # create a list of Document objects
    documents = [Document(page_content=doc.get('text'), metadata=doc.get('metadata')) for doc in documents_data]
            
    # remove json
    os.remove(json_file_path)
    

    # save in chromadb folder
    vector_dir = project_root + "chromadb/VectorStore"

    import time
    # initialize the vector store/db
    embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
    '''
    '''
    Chroma.from_documents(
            documents,
            embedding_function,
            persist_directory=vector_dir, # save in chromadb folder
        )


def get_rag_response(query, languageBool):

    eval = False
    if eval:
        write_rag_results()
        return

    print("Getting RAG response...")

    # save in chromadb folder
    vector_dir = "../../backend/chromadb/VectorStore" # from server dir
    #vector_dir = "chromadb" # running from this file

    # initialize the vector store/db
    embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
    db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder

    retriever = db.as_retriever(search_kwargs={"k": 4}) # k=3 => 4 sources
    #gemma:7b-instruct-v1.1-q8_0
    llm = Ollama(model="gemma")
    
    
    prompt = prompty(languageBool)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", 
        retriever=retriever, # 3 sources
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    result = qa.invoke(query)
    answer = result["result"]
    sources = result["source_documents"]
    print("-----------------------------------------------------------------------------------------------------------------------")
    print(query)
    print("ANSWER")
    print(answer)
    print("SOURCES")
    metadata = []
    pageContents = []
    for source in sources:
        print("")
        print("Source: ", source.metadata.get('source'))
        dataString =  source.metadata.get('source') + ", " + "p." + str(source.metadata.get('page'))
        pageContent = source.page_content
        pageContents.append(pageContent)
        metadata.append(dataString)
    print(metadata)
    print(pageContents)
    page_contents = pageContents
    print(answer)



    return answer, metadata, page_contents


def rag_qstar(query, languageBool):
    vector_dir = "../../backend/chromadb/VectorStore" # from server dir
    embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
    db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder
    retriever = db.as_retriever(search_kwargs={"k": 4}) # k=3 => 4 sources
    #gemma:7b-instruct-v1.1-q8_0
    llm = Ollama(model="gemma")
    prompt = prompty(languageBool)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", 
        retriever=retriever, # 3 sources
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    result = qa.invoke(query)
    answer = result["result"]
    sources = result["source_documents"]
    metadata = []
    pageContents = []
    for source in sources:
        dataString =  source.metadata.get('source') + ", " + "p." + str(source.metadata.get('page'))
        pageContent = source.page_content
        pageContents.append(pageContent)
        metadata.append(dataString)
    page_contents = pageContents
    return answer, metadata, page_contents
    
    


evalQuestions = [
    "How can one gain better control over my emotions?",
    "How can I increase my productivity?",
    "How can I enhance my focus?",
    "Why is continuous learning important for personal development?",
    "How can one overcome the fear of failure?",
    "What routines can I do to improve my mental health?",
    "What are the key factors in building successful business partnerships?",
    "How do you identify the right business partner for a startup?",
    "How do I get happier?",
    "How can setting personal goals contribute to a sense of fulfillment?",
    "What are the biggest challenges in establishing partnerships?",
    "How can one find a balance between work and free time to maximize happiness?",
    "How do I find a life partner?",
    "What habits should I form to be happier?",
    "What habits should I avoid?",
    "How do I form a new habit?",
    "How should I raise my kids?",
    "How do I break a bad habit?",
    "How do I enhance my learning capabilities?",
    "What are some good techniques for learning?",
]



import csv

def get_rag_response2(query, languageBool):
    print("Getting RAG response...")

    # save in chromadb folder
    vector_dir = "../../backend/chromadb/VectorStore" # from server dir
    #vector_dir = "chromadb" # running from this file

    import time
    # initialize the vector store/db
    embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
    db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder

    retriever = db.as_retriever(search_kwargs={"k": 4}) # k=3 => 4 sources
    llm = Ollama(model="llama3")
    
    prompt = prompty(languageBool)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", 
        retriever=retriever, # 3 sources
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    result = qa.invoke(query)
    answer = result["result"]
    sources = result["source_documents"]
    
    print("-----------------------------------------------------------------------------------------------------------------------")
    print(query)
    print("ANSWER")
    print(answer)
    print("SOURCES")
    metadata = []
    pageContents = []
    for source in sources:
        print("")
        print("Source: ", source.metadata.get('source'))
        dataString =  source.metadata.get('source') + ", " + "p." + str(source.metadata.get('page'))
        pageContent = source.page_content
        pageContents.append(pageContent)
        metadata.append(dataString)
    print(metadata)
    page_contents = pageContents
    
    return answer, metadata, page_contents


def write_rag_results():
    # open CSV file for writing
    with open('rag_results.csv', 'w', newline='') as csvfile:
        # create a CSV writer
        csvwriter = csv.writer(csvfile)

        # write header row
        csvwriter.writerow(['Question', 'Answer', 'Page Contents', 'Metadata'])

        # iterate over eval questions
        for question in evalQuestions:
            # get RAG response
            answer, metadata, page_contents = get_rag_response2(question, True)

            # question, answer, page contents, and metadata to CSV file
            csvwriter.writerow([question, answer, page_contents, metadata])