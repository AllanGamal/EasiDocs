from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
def deleteDocumentsBySourceFromDb(db, source):
    ids_to_delete = []

    ids = db.get(where = {'source': source})['ids']
    for id in ids:
        ids_to_delete.append(id)
    db.delete(ids_to_delete)


embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")
vector_dir = "chromadb/VectorStore"
db = Chroma(persist_directory=vector_dir, embedding_function=embedding_function) # load from the saved folder

deleteDocumentsBySourceFromDb(db, "pdf/ark.pdf")