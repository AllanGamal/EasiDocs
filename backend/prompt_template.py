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
If there is no direct, obvious or clear connection between the context and the question, say so clearly and then bring up and state potential connections between the context and the question. Explore potential links!
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

template2 = '''
'{question}'
'
{context}
'
%s
%s

IMPORTANT, DO NOT SAY A SINGLE WORD. BE SILENT. DO NOT RESPOND. DO NOT SAY ANYTHING!!! NOT A SINGLE WORD!
'''

def prompt2(languageBool):

    language = set_language(languageBool)
    
    prompt = PromptTemplate(
        template=template2 % (persona, language),
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