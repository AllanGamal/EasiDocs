from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from Embeddings import MiniLMEmbeddings
from LocalLLM import LocalLLM
from langchain_community.document_loaders import PyPDFLoader
import chromadb
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# import
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from transformers import AutoTokenizer, AutoModel



# initializing the embeddings
embeddings = MiniLMEmbeddings()


llm = Ollama(model="mistral")


def loader(file):
    loader = PyPDFLoader(file)
    documents = loader.load()
    return documents

document = loader("test.pdf")
##print(document)
print("---------------------------------------------------------")

# Extracting text from the document and returning it as a string
def extract_text(document):
    raw_text = ''
    for i, page in enumerate(document):
        raw_text += f"\nPage {i+1}\n" + "---------------------------------------------------------\n" # print the page number
        content = page.page_content
        raw_text += content
    return raw_text

raw_text = extract_text(document)
#print(raw_text)

# Text Splitter
#This takes the text and splits it into chunks. The chunk size is characters not tokens
def split_doc(document, chunk_size=1000, chunk_overlap=120): # 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = text_splitter.split_documents(document)
    return docs


docs = split_doc(document)
print("---------------------------------------------------------")
print("---------------------------------------------------------")
"""
def collect_page_contents(docs):
    split_text = []
    for doc in docs:
        split_text.append(doc.page_content)
    return split_text
"""


##dirty_split_text = collect_page_contents(docs)

def clean_docs(docs):
    for doc in docs:
        doc.page_content = doc.page_content.replace("\n", " ").replace("\t", " ")
    


clean_docs(docs)
print("---------------------------------------------------------")
print("---------------------------------------------------------")
# print type of docs
print(type(docs[0]))    

def listOfAllThePageContents(docs):
    page_contents = []
    for doc in docs:
        page_contents.append(doc.page_content)
    return page_contents

page_contents = listOfAllThePageContents(docs)

chroma_client = chromadb.Client()

docs_embeddings = embeddings.embed_documents(docs)


#embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")

#print(docs[0])


db = Chroma.from_documents(
    docs,
    embedding_function,
    
)

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




'''
collection = chroma_client.create_collection(name="my_collection")

#db = chromadb.Chroma.from_documents()
def add_documents_to_collection(docs, docs_embeddings, collection):
    for i, (doc, embedding) in enumerate(zip(docs, docs_embeddings)):
        # i used for the doc_id  
        doc_id = str(i)

        collection.add(
            ids=[doc_id],  # doc ID
            documents=[doc.page_content],  # doc text
            embeddings=[embedding.tolist()],  # convert to numpy array, then to list
            metadatas=[doc.metadata]  # metadata
        )


add_documents_to_collection(docs, docs_embeddings, collection)



print(docs_embeddings)

db = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings
)


chain = load_qa_chain(llm, chain_type="stuff")

def get_answer(query):
    # get two closest chunks
    answer = collection.query(
        query_texts=[query],
        n_results=1
    )
  
    return answer
    
print("Doc chatbot, chat with your docs!")
prompt = input("Ask a question about your docs: ")

if prompt:
    answer = get_answer(prompt)
    print(f"Answer: {answer}")   
'''