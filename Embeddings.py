from transformers import AutoTokenizer, AutoModel
import torch

class MiniLMEmbeddings:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Multilingual-MiniLM-L12-H384")
        self.model = AutoModel.from_pretrained("microsoft/Multilingual-MiniLM-L12-H384")
    
    def embed_documents(self, documents):
        # prepare inputs and generate embeddings
        embeddings = []
        for doc in documents:
            # extrhakt text from each document
            text = doc.page_content if hasattr(doc, 'page_content') else ""
            encoded_input = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
            with torch.no_grad():
                output = self.model(**encoded_input)
                # Take average of the embeddings and add to the list
                embeddings.append(output.last_hidden_state.mean(dim=1))
        return torch.stack(embeddings).squeeze()

# initializing the embeddings
embeddings = MiniLMEmbeddings()