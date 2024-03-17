from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
import os
'''
def deleteDocumentsBySourceFromDb(db, source):
    ids_to_delete = []
    test = "backend/pdf"
    for filename in os.listdir(test):
        print(filename)
    ids = db.get(where = {'source': source})['ids']
    for id in ids:
        print(id)
        ids_to_delete.append(id)
    db.delete(ids_to_delete)


embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
vector_dir = "backend/chromadb/VectorStore"
db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder

deleteDocumentsBySourceFromDb(db, "pdf/ark.pdf")

'''
import os
def deleteDocumentsBySourceFromDb(source):
    
    ids_to_delete = []
    vector_dir = "../../backend/chromadb/VectorStore" # from server dir
    
    # print this directory of this file
    
    embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
    db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder
    ids = db.get(where = {'source': source})['ids']
    print(ids)
    for id in ids:
        ids_to_delete.append(id)
    db.delete(ids_to_delete)



# deleteDocumentsBySourceFromDb(db, "pdf/ark.pdf")
