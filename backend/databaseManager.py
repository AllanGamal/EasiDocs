from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

import os

def deleteDocumentsBySourceFromDb(source):
    
    filename = os.path.basename(source)
    base_root = "../../backend/"
    print("Deleting filename: " + filename + " with source: " + base_root + source)
    ids_to_delete = []
    vector_dir = "../../backend/chromadb/VectorStore" # from server dir
    embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
    db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder
    ids = db.get(where = {'source': filename})['ids']
    for id in ids:
        ids_to_delete.append(id)
    db.delete(ids_to_delete)
'''
def deleteDocumentsBySourceFromDb(source):
    base_root = ""
    ids_to_delete = []
    print("Deleting documents with source: ", base_root + source)
    # print this directory
    vector_dir = "chromadb/VectorStore" # from server dir
    # print all files in the directory
    embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
    db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder
    ids = db.get(where = {'source': base_root + source})['ids']
    for id in ids:
        print("Deleting document with id: ", id)
        ids_to_delete.append(id)
    db.delete(ids_to_delete)

'''
# deleteDocumentsBySourceFromDb(db, "pdf/ark.pdf")
