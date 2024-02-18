from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from Embeddings import MiniLMEmbeddings
from localLLM import LocalLLM
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader



# initializing the embeddings
embeddings = MiniLMEmbeddings()


llm = LocalLLM(base_url="http://localhost:1234/v1")


def loader(file):
    loader = PyPDFLoader(file)
    documents = loader.load()
    return documents

document = loader("test.pdf")
print(document)
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
print(raw_text)

# Text Splitter
#This takes the text and splits it into chunks. The chunk size is characters not tokens
def split_doc(document, chunk_size=900, chunk_overlap=90): # 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = text_splitter.split_documents(document)
    return docs


docs = split_doc(document)
print("---------------------------------------------------------")
print(docs[0])
print(docs[1])

print("---------------------------------------------------------")
docs_embeddings = embeddings.embed_documents(docs)

db = Chroma.from_documents(
    documents=docs_embeddings, 
    embedding=embeddings
)

chain = load_qa_chain(llm, chain_type="stuff")

def get_answer(query):
    similar_docs = db.similarity_search(query, k=2) # get two closest chunks
    answer = chain.run(input_documents=similar_docs, question=query)
    return answer
    
print("Doc chatbot, chat with your docs!")
prompt = input("Ask a question about your docs: ")

if prompt:
    answer = get_answer(prompt)
    print(f"Answer: {answer}")   