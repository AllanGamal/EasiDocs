class LocalLLM:
    def __init__(self, base_url="http://localhost:1234/v1"):
        # Konfigurera klienten att peka mot din lokala server
        self.client = openai.OpenAI(base_url=base_url, api_key="not-needed")

    def answer_question(self, question, context=None):
        # Använd din lokala LLM för att generera ett svar på frågan
        try:
            completion = self.client.chat.completions.create(
                model="local-model",  # Detta fält används för närvarande inte men kan behövas för framtida anpassningar
                messages=[
                    {"role": "system", "content": "Your system message here, if any."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,  # Justera efter behov för att styra kreativiteten i svaren
            )
            
            return completion.choices[0].message.content 
        except Exception as e:
            print(f"An error occurred: {e}")
            return "I'm sorry, I encountered an error and can't provide an answer."

# Skapa en instans av din anpassade klass
llm = LocalLLM()

