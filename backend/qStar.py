
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from RAG import rag_qstar, get_rag_response
# Example: reuse your existing OpenAI setup
from openai import OpenAI
# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")



class Node:
    top_10_nodes = []
    previous_questions = []
    previous_ids = []
    longest_branch = ""
    n_nondes_explored = 0
    n_previous_explored_nodes = 0
    def __init__(self, question, context, confidence, level, query_number,  sibling_number, full_branch,branch_path=[],  parent=None):
        self.question = question
        self.context = context
        self.confidence = confidence
        self.level = level
        self.query_number = query_number
        self.sibling_number = sibling_number
        if branch_path is None:
            self.branch_path = []  
        else:
            self.branch_path = list(branch_path) 

        if parent is not None:
            self.branch_path.append("q" + str(query_number) + "b" + str(sibling_number))
        self.parent = parent
        self.children = []
        self.explored = False
        self.full_branch = full_branch

    def add_child(self, question, context, confidence, query_number, sibling_number, full_branch):
        child_node = Node(question, context, confidence, self.level + 1, query_number, sibling_number, full_branch, self.branch_path, self)
        self.children.append(child_node)
        return child_node
    
    def get_question_path(self):
        node = self
        path = []
        while node is not None:
            path.append(f"lvl{node.level}q{node.query_number}b{node.sibling_number}, query: {node.question}, cl: {node.confidence}")
            node = node.parent
        return path[::-1]

    def get_full_branch(self):
        return self.full_branch
    
    def get_number(self):
        return self.query_number
        

    def get_children(self):
        return self.children
    
    def get_context(self):
        return self.context
    
    def get_confidence(self):
        return self.confidence
    
    def set_context(self, context):
        self.context = context

    def set_confidence(self, confidence):
        self.confidence = confidence
    
    def is_goal_reached(self, tresholad_confidence_level=0.85):
        return self.confidence > tresholad_confidence_level
    
    def get_ancestors(self):
        
        node = self
        ancestors = []
        while node:
            ancestors.append(node)
            node = node.parent
        return ancestors[::-1]  
    
    def display_ancestry(self):
        ancestry = self.get_ancestors()
        for ancestor in ancestry:
            print(f"q{ancestor.level},{ancestor.number} - {ancestor.question} - Confidence: {ancestor.confidence}")
    
    def get_level(self):
        return self.level
    
    @staticmethod
    def update_explored_nodes():
        Node.n_nondes_explored += 1

    @staticmethod
    def update_previous_explored_nodes():
        Node.n_previous_explored_nodes += 1
    
    @staticmethod
    def get_n_previous_explored_nodes():
        return Node.n_previous_explored_nodes
    
    @staticmethod
    def get_previous_ids():
        return Node.previous_ids
    
    def update_previous_ids(id):
        Node.previous_ids.append(id)

    @staticmethod
    def update_longest_branch(branch):
        if len(branch) >= len(Node.longest_branch):
            Node.longest_branch = branch
    
    @staticmethod
    def get_longest_branch():
        return Node.longest_branch
    
    
    @staticmethod
    def update_top_10_nodes(node):
        if len(Node.top_10_nodes) < 10:
            Node.top_10_nodes.append(node) 
        else:
            min_confidence_node = min(Node.top_10_nodes, key=lambda node: node.confidence)
            if node.confidence > min_confidence_node.confidence:
                # node with higher confidence => replace node with lowest confidence
                Node.top_10_nodes.remove(min_confidence_node)
                Node.top_10_nodes.append(node)
        
        Node.top_10_nodes = sorted(Node.top_10_nodes, key=lambda node: node.confidence, reverse=True) # sort the list (desc)

    @staticmethod
    def get_top_10_nodes():
        return Node.top_10_nodes

    @staticmethod
    def add_to_previous_questions(question):
        Node.previous_questions.append(question)

    @staticmethod
    def get_previous_questions():
        return Node.previous_questions
    

def get_llm_response(prompt):
    completion = client.chat.completions.create(
        model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful. You will never reason from your own knowledge, only deduce from the context and question provided. Never use the '*' character."},
    {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )
    return completion.choices[0].message.content


def get_answer(question, context):
    template = '''
    Never quote sources.
    Question: '{question}'
    Context:
    '
    {context}
    '

    Make a detailed answer, based on the context and the question {question}.
    If there is no direct, obvious or clear connection between the context and the question, say clearly and then bring up and state potential connections between the context and the question, even if it is somewhat far stretched anv vague. 
    Only deduce connections from the context and question provided.
    Be creative and explore potential links!
    '''

    prompt = template.format(question=question, context=context)

    return get_llm_response(prompt)
    
    
    

    
def generate_new_query(goal, node):
    context = node.get_context()
    previous_questions = Node.get_previous_questions()
    prompt = f"With the objective in mind on the mind: '{goal}', what kind of a general question about the context do you think could be the answer the objective? Context: '{context}'. Dont generate any questions that is same or similar to the previous questions. Previous questions that must not be repeated or must not be similar: '{previous_questions}'. The question could be more general about the objective, but must be super short and super concise, and relevant (directly or inderectly) to the context and objective. Dont reason how to get the question, just state the question in one short sentence. Remember, Dont generate any questions that is same or similar to the previous questions, and keep it short."
    new_query = get_llm_response(prompt)
    return new_query


def generate_new_queries(goal, node, number_of_queries=4):
    new_queries = []
    for i in range(number_of_queries):
        query = generate_new_query(goal, node)
        new_queries.append(query)
        Node.add_to_previous_questions(query)
    print(new_queries)
    return new_queries


def evaluate_confidence_level(goal, context, query):
    prompt = f'''Based on the goal '{goal}', how confident are you that this context could be relevant to the goal? Context: '{context}'. 
    Respond solely with a confidence level as a float between 0.00 and 1.00, where 0.00 indicates no confidence and 1.00 indicates complete confidence in the context's relevance to the goal. 
    Your answer must strictly be a single numerical float, e.g., '0.51', '0.72' and so on. Do not include any text or other characters other than the float.'''
    #llm = Ollama(model="gemma")
    #confidence_level = float(llm.invoke(prompt))
    confidence_level = float(get_llm_response(prompt))
    print("---------------------------------------------------------")
    print(f"Goal: {goal}")
    print(f"Query: {query}")
    print(f"Context: {context}")
    print(f"Confidence level: {confidence_level}")
    return confidence_level
    
   

def root_qStar(goal, context):
    meta, contents = rag_qstar(goal, languageBool=True)
    context = " ".join(contents)
    print(f"Context: {context}")
    root_node = Node(goal, context, 0.0, 0, 0, 0, "")
    result = qStar(root_node, goal)
    # print top 10 nodes
    all_nodes = Node.get_top_10_nodes()
    contexts = [node.context for node in all_nodes]
    context = " "
    context = " ".join(contexts)
    for node in all_nodes:
        print(f"Top 10 nodes: {node.confidence}")

    print("---------------------------------HORRAY---------------------------------")
    print("---------------------------------HORRAY---------------------------------")
    print(f"Number of Explored nodes: {Node.n_nondes_explored}")
    print(f"Number of Previous explored nodes: {Node.n_previous_explored_nodes}")
    print(f"Context: {context}")
    print("---------------------------------HORRAY---------------------------------")
    print("---------------------------------HORRAY---------------------------------")
    answer = get_answer(goal, context)
    return answer, ["test", "test2"], contexts


    
def qStar(current_node, goal, depth_limit=7):
    if depth_limit == 0 or current_node.is_goal_reached() or current_node.explored:

        return current_node
    

    current_node.explored = True

    # explore child
    result = explore_child_nodes(current_node, goal, depth_limit)
    if result:
        print(f"Goal reached at level {result.get_level()}")
        return result
                
    # no child valid => iterate over highest confidence leveled siblings
    result = handle_sibling_nodes(current_node, goal, depth_limit)
    if result:
        print(f"Goal reached at level {result.get_level()}")
        return result

    
    return None

def explore_child_nodes(current_node, goal, depth_limit):
    child_nodes = generate_child_nodes(current_node, goal)
    if child_nodes:
        # sort children
        sorted_children = sorted(child_nodes, key=lambda node: node.confidence, reverse=True)
        print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        for sort_child in sorted_children:
            print(sort_child.confidence)
        if sorted_children[0].is_goal_reached(): # answer found 
            return sorted_children[0]
        for child in sorted_children:
            if child.confidence > current_node.confidence * 0.9 and not child.explored: 
                result = qStar(child, goal, depth_limit - 1)
                if result and result.is_goal_reached():
                    return result
    return None



def generate_child_nodes(current_node, goal):
    new_queries = generate_new_queries(goal, current_node)
    print(f"New queries: {new_queries}")
    child_nodes = []
    for query in new_queries:
        query_number = new_queries.index(query) + 1
        print("test")
        query_result = rag_qstar(query, languageBool=True)
        if query_result is None:
            continue  # Skip if no result
        ids, contexts = query_result  # Unpacking three values, ignore the third if not needed
        for context_index, context in enumerate(contexts):
            Node.update_explored_nodes()
            
            if ids[context_index] in Node.get_previous_ids():
                Node.update_previous_explored_nodes()
                print(f"Skipping child node with repeated id '{ids[context_index]}', with the branch path {current_node.branch_path}, q{query_number}b{context_index + 1}")
                continue
            confidence = evaluate_confidence_level(goal, context, query)
            if confidence <= 0.15:
                print(f"Skipping child node with confidence {confidence}, with the branch path {current_node.branch_path}, q{query_number}b{context_index + 1}")
                continue
            Node.update_previous_ids(ids[context_index])  
            branch_descriptor = ','.join(f'{b}' for b in current_node.branch_path)
            full_branch = f"lvl{current_node.level + 1},{branch_descriptor} q{query_number}b{context_index + 1}"
            child_node = current_node.add_child(query, context, confidence, query_number, context_index + 1, full_branch)
            Node.update_longest_branch(full_branch)
            print(f"Creating child node: {full_branch} with confidence {confidence}")
            if child_node.is_goal_reached():
                question_path = child_node.get_question_path()
                print("---------------------------------HORRAY---------------------------------")
                print("---------------------------------HORRAY---------------------------------")
                print(f"Goal reached at level {full_branch}")
                print(f"Longest branch: {Node.get_longest_branch()}")
                print(f"Question path: {question_path}")
                print(f"Number of Explored nodes: {Node.n_nondes_explored}")
                print("---------------------------------HORRAY---------------------------------")
                print("---------------------------------HORRAY---------------------------------")
            child_nodes.append(child_node)
            Node.update_top_10_nodes(child_node)
            

    return child_nodes

 


def handle_sibling_nodes(current_node, goal, depth_limit):
    if current_node.parent is None or depth_limit <= 0:
        # If there is no parent or depth limit has been exhausted, return None
        return None

    if current_node.parent and depth_limit > 0:
        siblings = [sib for sib in current_node.parent.children if sib != current_node and not sib.explored]
        sorted_siblings = sorted(siblings, key=lambda node: node.confidence, reverse=True)
        for sibling in sorted_siblings:
            result = qStar(sibling, goal, depth_limit)
            if result and result.is_goal_reached():
                return result
    return None
