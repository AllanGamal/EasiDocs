
from langchain_community.llms import Ollama
from RAG import rag_qstar
previous_questions = []
goal_reached = False
prompt_template = "Based on the goal of {goal}, what question would you ask to get there? That is not already in the list of previous questions {previousQuestions}"



class Node:
    top_10_nodes = []
    previous_questions = []
    def __init__(self, question, context, confidence, level, parent=None):
        self.question = question
        self.context = context
        self.confidence = confidence
        self.level = level
        self.parent = parent
        self.children = []

    def add_child(self, question, context, confidence):
        child_node = Node(question, context, confidence, self.level + 1, self)
        self.children.append(child_node)
        return child_node
        

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
        return self.confidence >= tresholad_confidence_level
    
    def get_ancestors(self):
        """ Returns a list of ancestor nodes leading up to this node, including the current node. """
        node = self
        ancestors = []
        while node:
            ancestors.append(node)
            node = node.parent
        return ancestors[::-1]  
    
    def display_ancestry(self):
        ancestry = self.get_ancestors()
        for ancestor in ancestry:
            print(ancestor)
    
    def get_level(self):
        return self.level
    
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
    def add_to_previous_questions(question):
        Node.previous_questions.append(question)

    @staticmethod
    def get_previous_questions():
        return Node.previous_questions


    
    
    
def generate_new_query(goal, node):
    prompt = f"With the objective in mind on the mind: {goal}, what question about the context do you think would answer the objective? Context: {node.get_context}. Dont use any questions that is too similar to the previous questions. Previous questions: '{Node.get_previous_questions}'. You have to answer in a question format. The question should be super short and super concise, and relevant to the context and objective. Remember, keep it short"
    llm = Ollama(model="gemma")
    new_query = llm.invoke(prompt)
    return new_query

def generate_new_queries(goal, node, number_of_queries=2):
    new_queries = []
    for i in range(number_of_queries):
        query = generate_new_query(goal, node)
        new_queries.append(query)
        Node.add_to_previous_questions(query)
    print(new_queries)
    return new_queries


def evaluate_confidence_level(goal, context):
    prompt = f'''Based on the goal of {goal}, how confident are you that this context is relevant to the goal? Context: {context}. 
    Respond solely with a confidence level as a float between 0.0 and 1.0, where 0.0 indicates no confidence and 1.0 indicates complete confidence in the context's relevance to the goal. 
    Your answer must strictly be a numerical float, e.g., '0.5', '0.75'. Do not include any text or other characters.'''
    llm = Ollama(model="gemma")
    confidence_level = float(llm.invoke(prompt))
    print(f"Goal: {goal}")
    print(f"Context: {context}")
    print(f"Confidence level: {confidence_level}")
    print("")
    return confidence_level

def root_qStar(goal, context):
    root_node = Node(goal, context, 0, 0)
    return qStar(root_node, goal)


    
def qStar(current_node, goal, depth_limit=10):
    if depth_limit == 0 or current_node.is_goal_reached():
        return current_node
    
    print(f"Exploring from node: {current_node.get_level()} {current_node.question} with confidence {current_node.confidence}")

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

    # 
    return None

def explore_child_nodes(current_node, goal, depth_limit):
    child_nodes = generate_child_nodes(current_node, goal)
    if child_nodes:
        # sort children
        sorted_children = sorted(child_nodes, key=lambda node: node.confidence, reverse=True)
        if sorted_children[0].is_goal_reached(): # answer found 
            return sorted_children[0]
        for child in sorted_children:
            if child.confidence > current_node.confidence * 0.9: 
                result = qStar(child, goal, depth_limit - 1)
                if result and result.is_goal_reached():
                    return result
    return None

def generate_child_nodes(current_node, goal):
    new_queries = generate_new_queries(goal, current_node.get_context())
    child_nodes = []
    for query in new_queries:
        query_result, metadata, contexts = rag_qstar(query, languageBool=True)
        for context in contexts:
            confidence = evaluate_confidence_level(goal, context)
            if confidence < 0.15:
                continue
            child_node = current_node.add_child(query, context, confidence)
            child_nodes.append(child_node)
            Node.update_top_10_nodes(child_node) 
    return child_nodes


def handle_sibling_nodes(current_node, goal, depth_limit):
    if current_node.parent: 
        siblings = [sib for sib in current_node.parent.children if sib != current_node] # 
        sorted_siblings = sorted(siblings, key=lambda node: node.confidence, reverse=True)
        for sibling in sorted_siblings:
            result = qStar(sibling, goal, depth_limit - 1)
            if result and result.is_goal_reached():
                return result
    return None


