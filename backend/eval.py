from RAG import run_maven, load_document_batch, get_rag_response

from langchain_community.document_loaders import DirectoryLoader
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context, conditional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.llms import Ollama


import os
os.environ["OPENAI_API_KEY"] = "Ur API key here"




loader = DirectoryLoader("eval")
print("loader")

documents = loader.load()
for document in documents:
    document.metadata['filename'] = document.metadata['source']

print("loader done")

print(documents[0])

generator_llm = Ollama(model="mistral")
critic_llm = Ollama(model="mistral")
# critic_llm = ChatOpenAI(model="gpt-4")
embeddings = OpenAIEmbeddings()

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings
)
print("test1")
generator.adapt(language="english",evolutions=[simple, multi_context, conditional, reasoning])
print("test2")
generator.save(evolutions=[simple, multi_context, reasoning, conditional])
print("test3")
testset = generator.generate_with_langchain_docs(documents, test_size=10, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25})
testset.to_pandas()

# show the testset

print(testset.to_pandas())
print("testset done")

# save the testset
