from langchain.prompts import PromptTemplate



template = '''
If you don't know the answer, just say that you don't know.
Don't try to make up an answer. Answer ONLY in whatever language you get the question in.
Never quote sources.
{context}

%s

Question: {question}
Answer in %s :
'''

persona = ""  #+ "Respond in the persona of a extremely depressed and sarcastic robot!"

def prompt(languageBool):

    language = set_language(languageBool)
    
    prompt = PromptTemplate(
        template=template % (persona, language),
        input_variables=[
            'context', 
            'question'
        ]
    )
    return prompt


def set_language(bool):
    if bool:
        return "English"
    return "Swedish"