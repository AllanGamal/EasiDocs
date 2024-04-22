'''
# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
  messages=[
    {"role": "system", "content": "Always answer in rhymes."},
    {"role": "user", "content": "Introduce yourself."}
  ],
  temperature=0.0,
)

print(completion.choices[0].message.content)
'''
from sentence_transformers import SentenceTransformer


path = "/Users/allangamal/Documents/GitHub/EasiDocs/backend/eval/testy"
print("Loading model")
model = SentenceTransformer("intfloat/multilingual-e5-large")
print("Model loaded")
model.save(path)

