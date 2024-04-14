from langchain.prompts import PromptTemplate



template = '''
Never quote sources.
Question: '{question}'
Context:
'
{context}
'
%s

Make a detailed answer, based on the context, in %s. 
If there is no direct, obvious or clear connection between the context and the question, say clearly and then bring up and state 1 potential connections between the context and the question, even if it is somewhat far stretched anv vague. Be creative and explore potential links!
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