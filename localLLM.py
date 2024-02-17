import openai

class LocalLLM:
    def __init__(self, base_url="http://localhost:1234/v1"):
        # Client config
        self.client = openai.OpenAI(base_url=base_url, api_key="not-needed")

    def answer_question(self, question, context=None):
        
        try:
            completion = self.client.chat.completions.create(
                model="local-model",  # the name of  local model
                messages=[
                    {"role": "system", "content": "Your system message here, if any."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,  # creativity meter
            )
            
            return completion.choices[0].message.content 
        except Exception as e:
            print(f"An error occurred: {e}")
            return "I'm sorry, I encountered an error and can't provide an answer."

# Skapa en instans av din anpassade klass
llm = LocalLLM()

'''
question = "What is the capital of Sweden?"
answer = llm.answer_question(question)
print(f"Answer: {answer}")
'''