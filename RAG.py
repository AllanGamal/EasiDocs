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
from langchain.prompts import PromptTemplate



llm = Ollama(model="mistral")


document = document_ingestion.load_document("test.pdf")
#documents = load_document_batch(["test.pdf", "test.docx", "test.txt"])
#document = load_document("test.txt")


docs = document_ingestion.split_document(document)

document_ingestion.clean_documents(docs)


page_contents = document_ingestion.get_page_contents(docs)

embedding_function = SentenceTransformerEmbeddings(model_name="intfloat/multilingual-e5-large")


# initialize the vector store/db
db = Chroma.from_documents(
        docs,
        embedding_function
    )




query_en = "What kind of technologies are reshaping education systems? "
query_sv = "Vilka teknologier omformar utbildningssystemen?"


template = '''
If you don't know the answer, just say that you don't know.
Don't try to make up an answer. Answer ONLY in whatever language you get the question in.
Never quote sources.
{context}

%s

Question: {question}
Answer in %s :
'''

persona = "" #"Respond in the persona of a goofy person"
language = ["Swedish", "English"]
prompt = PromptTemplate(
    template=template % (persona, language[1]),
    input_variables=[
        'context', 
        'question'
    ]
)

retriever = db.as_retriever(search_kwargs={"k": 3}) # k=3 => 3 sources

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=retriever, # 3 sources
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)


result = qa.invoke(query_sv)

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

