import openai
from langchain.llms import BaseLLM


# If using LLM through the LMstudo 
class LocalLLM(BaseLLM):
    def __init__(self, base_url="http://localhost:1234/v1"):
        super().__init__()
        self.client = openai.OpenAI(base_url=base_url, api_key="not-needed")

    def _generate(self, prompt, **kwargs):
        
        try:
            completion = self.client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "system", "content": "Your system message here, if any."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # Anpassa efter behov
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def _llm_type(self):
        
        return "LocalLLM"

    
    def run(self, prompt, **kwargs):
        return self._generate(prompt, **kwargs)
