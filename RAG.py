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



llm = Ollama(model="mistral")


#document = document_ingestion.load_document("ark.pdf")
#documents = load_document_batch(["test.pdf", "test.docx", "test.txt"])
# load all documents in a folder

#documents = document_ingestion.load_documents_from_folder("pdf")
# define the documents

print("–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

documents = load_document_batch(["pdf/test.pdf"])



# cocument splitting and cleaning (running java code)
def run_maven():
    command = ['mvn', 'exec:java', '-Dexec.mainClass=com.rag.Main']
    project_root = 'rag'
    process = subprocess.Popen(command, cwd=project_root)
    process.wait()
     
run_maven()


'''
documents = document_ingestion.load_document_batch(["pdf/22.pdf", "pdf/33.pdf", "pdf/46.pdf", "pdf/64.pdf", "pdf/180.pdf", "pdf/ark.pdf", "pdf/test.pdf"]) 
docs = document_ingestion.split_document_batch(documents)
document_ingestion.clean_documents(docs)
'''


#docs = document_ingestion.split_document(document)
#page_contents = document_ingestion.get_page_contents(docs)

embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")

# save in chromadb folder
vector_dir = "chromadb/VectorStore"

import time
start = time.time()
# initialize the vector store/db
'''
db = Chroma.from_documents(
        docs,
        embedding_function,
        persist_directory=vector_dir, # save in chromadb folder
    )
'''




db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder




retriever = db.as_retriever(search_kwargs={"k": 3}) # k=3 => 3 sources

prompt = prompt()
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=retriever, # 3 sources
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)
end = time.time()
print("Time elapsed: ", end - start)


#query_en = "What kind of technologies are reshaping education systems? "
query_en = "Why are EV manufacturers retracting from the EV market"
query_sv = "Vilka teknologier omformar utbildningssystemen?"
query2_en = "Have AR or VR revealed any potential in the education sector?"
print("QUESTION")
print(query_en)


result = qa.invoke(query_en)

answer = result["result"]
sources = result["source_documents"]


print("-----------------------------------------------------------------------------------------------------------------------")
print("ANSWER")
print(answer)
print(len(sources))
print("SOURCES")
for source in sources:
    print("-----------------------------------------------------------------------------------------------------------------------")
    print(source)
    print("-----------------------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------------------")

# stop the timer
