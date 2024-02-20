from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
import document_ingestion as document_ingestion
from langchain.chains import RetrievalQA
from prompt_template import prompt as prompt



llm = Ollama(model="mistral")


document = document_ingestion.load_document("ark.pdf")
#documents = load_document_batch(["test.pdf", "test.docx", "test.txt"])
#document = load_document("test.txt")


docs = document_ingestion.split_document(document)

document_ingestion.clean_documents(docs)


page_contents = document_ingestion.get_page_contents(docs)

embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")

import time
start = time.time()
# initialize the vector store/db
db = Chroma.from_documents(
        docs,
        embedding_function
    )




retriever = db.as_retriever(search_kwargs={"k": 4}) # k=3 => 3 sources

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

result = qa.invoke(query_en)

answer = result["result"]
sources = result["source_documents"]


print("-----------------------------------------------------------------------------------------------------------------------")
print(answer)
print(len(sources))
for source in sources:
    print("-----------------------------------------------------------------------------------------------------------------------")
    print(source)
    print("-----------------------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------------------")

# stop the timer