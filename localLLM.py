import openai
from langchain.llms import BaseLLM

class LocalLLM(BaseLLM):
    def __init__(self, base_url="http://localhost:1234/v1"):
        super().__init__()
        self.client = openai.OpenAI(base_url=base_url, api_key="not-needed")

    def _generate(self, prompt, **kwargs):
        # Denna metod bör anropa OpenAI's API och returnera svaret
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
        # Denna metod bör returnera en sträng som representerar typen av LLM. Detta är ett exempel:
        return "LocalLLM"

    # 'run'-metoden kan behållas om den behövs för andra syften,
    # men '_generate'-metoden är den som används av 'BaseLLM' för att generera text.
    def run(self, prompt, **kwargs):
        return self._generate(prompt, **kwargs)
