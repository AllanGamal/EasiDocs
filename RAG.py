from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from Embeddings import MiniLMEmbeddings
from localLLM import LocalLLM
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter



# initializing the embeddings
embeddings = MiniLMEmbeddings()


llm = LocalLLM(base_url="http://localhost:1234/v1")


def loader(file):
    loader = PyPDFLoader(file)
    documents = loader.load()
    return documents

document = loader("test.pdf")
doc_reader = PdfReader('test.pdf')
print(document)
print("---------------------------------------------------------")
# read data from the file and put them into a variable called raw_text
raw_text = ''
for i, page in enumerate(document):
    raw_text += f"\nPage {i+1}\n" + "---------------------------------------------------------\n" # print the page number
    content = page.page_content
    raw_text += content
    
    
    

print(raw_text)




def split_docs(documents, chunk_size=500, chunk_overlap=50): # not working
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = text_splitter.split_documents(documents)
    return docs


docs = split_docs(doc_reader)
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