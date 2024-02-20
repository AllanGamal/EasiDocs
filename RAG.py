from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from LocalLLM import LocalLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
import document_ingestion as document_ingestion
import embedding as embedding




llm = Ollama(model="mistral")


document = document_ingestion.load_document("test.pdf")
#documents = load_document_batch(["test.pdf", "test.docx", "test.txt"])
#document = load_document("test.txt")


docs = document_ingestion.split_document(document)

document_ingestion.clean_documents(docs)


page_contents = document_ingestion.get_page_contents(docs)

embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")


db = Chroma.from_documents(
        docs,
        embedding_function,
    )


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



