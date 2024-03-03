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

print("–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
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
'''



# save in chromadb folder
vector_dir = "chromadb/VectorStore"

import time
# initialize the vector store/db
embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
'''
db = Chroma.from_documents(
        documents,
        embedding_function,
        persist_directory=vector_dir, # save in chromadb folder
    )
'''


db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder

retriever = db.as_retriever(search_kwargs={"k": 3}) # k=3 => 3 sources
db = 1
embedding_function = 1
llm = Ollama(model="mistral")
prompt = prompt()
start = time.time()
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=retriever, # 3 sources
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)
end = time.time()


#query_en = "What kind of technologies are reshaping education systems? "
query_en = "Why are EV manufacturers retracting from the EV market"
query_sv = "Vilka teknologier omformar utbildningssystemen?"
query2_en = "Have AR or VR revealed any potential in the education sector?"
print("QUESTION")
print(query_en)


result = qa.invoke(query_en)

answer = result["result"]
sources = result["source_documents"]
print("Time elapsed: ", end - start)


print("-----------------------------------------------------------------------------------------------------------------------")
print("ANSWER")
print(answer)
print(len(sources))
print("SOURCES")
for source in sources:
    print("-----------------------------------------------------------------------------------------------------------------------")
    print(source)
    print("-----------------------------------------------------------------------------------------------------------------------")


# stop the timer
