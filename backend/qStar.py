
from langchain_community.llms import Ollama
previous_questions = []
goal_reached = False
prompt_template = "Based on the goal of {goal}, what question would you ask to get there? That is not already in the list of previous questions {previousQuestions}"

class Node:
    def __init__(self, question, context, confidence, level, parent=None):
        self.question = question
        self.context = context
        self.confidence = confidence
        self.level = level
        self.parent = parent
        self.children = []

    def add_child(self, question, context, confidence):
        # Create a new node with level incremented by 1
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
        return ancestors[::-1]  # Reverse to start from the root
    
    def display_ancestry(self):
        ancestry = self.get_ancestors()
        for ancestor in ancestry:
            print(ancestor)
    
    def get_level(self):
        return self.level
    
    
def generate_new_query(goal, context):
    prompt = f"With the objective in mind on the mind: {goal}, what question about the context do you think would answer the objective? Context: {context}.  Dont use any questions that is too similar to the previous questions {previous_questions}. You have to answer in a question format. The question should be super short and super concise, and relevant to the context and objective. Remember, keep it short"
    llm = Ollama(model="gemma")
    new_query = llm.invoke(prompt)
    return new_query

def generate_new_queries(goal, context, number_of_queries=3):
    new_queries = []
    for i in range(number_of_queries):
        query = generate_new_query(goal, context)
        new_queries.append(query)
        previous_questions.append(query)
    print(new_queries)
    return new_queries

generate_new_queries("how do i get a wife?", "Based on the context provided, it appears you are looking for areas of aptitude and interest that could potentially lead to forming a meaningful relationship or finding a partner. While I cannot directly answer this question with a specific list due to its subjective nature, I can suggest some possible directions based on the text's emphasis on natural ability and deep personal interest. 1. Communication: Having excellent verbal and written communication skills is essential for building strong relationships. Being able to express your thoughts, feelings, and ideas effectively is crucial in forming meaningful connections with others. 2. Emotional Intelligence: The ability to understand and manage your own emotions, as well as those of others, is key to fostering healthy relationships. Empathy, compassion, and emotional resilience are essential qualities for building strong bonds with a partner. 3. Social Skills: Being outgoing, friendly, and able to connect with various types of people can increase your chances of meeting potential partners in different social settings. Having a wide circle of friends and acquaintances opens up more opportunities for forming romantic relationships. 4. Shared Interests: Pursuing activities that align with your personal interests and passions can lead you to meet like-minded individuals who may share similar values and goals. Joining clubs, attending workshops, or participating in events related to your interests can provide valuable opportunities to connect with potential partners. 5. Intellectual Curiosity: Being open-minded and curious about various topics can help broaden your horizons and increase the chances of meeting diverse individuals. Engaging in intellectual pursuits and engaging in thoughtful discussions with others can lead to deeper connections. 6. Emotional Resilience: The ability to bounce back from challenges, setbacks, and heartbreaks is vital for maintaining a healthy perspective on relationships. Developing emotional resilience through self-care practices, mindfulness, or therapy can help you navigate the ups and downs of romantic connections more effectively. 7. Cultural Sensitivity: Having an appreciation for diverse backgrounds, beliefs, and experiences can help you form meaningful connections with people from various cultural backgrounds. Being open to learning about different customs, traditions, and perspectives can lead to stronger bonds and deeper understanding.")



def evaluate_confidence_level(goal, context):
    prompt = f"Based on the goal of {goal}, how confident are you that this context is relevant to the goal? Context: {context}. Answer ONLY with a confidence level float between 0.0 and 1.0. You are not allowed to answer with anything other than a float. Please ONLY answer in a float format. For example, '0.5' or '0.75'."
    llm = Ollama(model="gemma")
    confidence_level = float(llm.invoke(prompt))
    print(f"Confidence level: {confidence_level}")
    return confidence_level

evaluate_confidence_level("how do i get a wife?", '''The provided text does not contain any direct or obvious information regarding finding a wife, so there is no direct connection between the context and the question.

**Potential connection:**

The text suggests that successful startup founders tend to be good people, implying that finding a partner who shares similar values and principles may be important for achieving success in work and life. This connection is somewhat far-fetched and does not provide specific guidance on how to find a wife.''')  


    
def qStar(current_node, goal, depth_limit=10):
    if depth_limit == 0 or current_node.is_goal_reached():
        return current_node
    
    print(f"Exploring from node: {current_node.get_level()} {current_node.question} with confidence {current_node.confidence}")

     # Assume generate_new_queries and evaluate_confidence are implemented
    child_nodes = generate_child_nodes(current_node, goal)

    # Proceed if there are child nodes generated
    result = explore_child_nodes(current_node, goal, depth_limit)
    if result:
        return result
                
            
    # If no child is valid and the node has siblings, iterate over siblings with the next highest confidence
    result = handle_sibling_nodes(current_node, goal, depth_limit)
    if result:
        return result

    # Return None if no progress can be made
    return None

def explore_child_nodes(current_node, goal, depth_limit):
    child_nodes = generate_child_nodes(current_node, goal)
    if child_nodes:
        # Sort children by confidence in descending order
        sorted_children = sorted(child_nodes, key=lambda node: node.confidence, reverse=True)
        for child in sorted_children:
            if child.confidence > current_node.confidence * 0.9:
                result = qStar(child, goal, depth_limit - 1)
                if result and result.is_goal_reached():
                    return result
    return None


def handle_sibling_nodes(current_node, goal, depth_limit):
    if current_node.parent:
        siblings = [sib for sib in current_node.parent.children if sib != current_node]
        sorted_siblings = sorted(siblings, key=lambda node: node.confidence, reverse=True)
        for sibling in sorted_siblings:
            if sibling.confidence > current_node.confidence * 0.9:
                result = qStar(sibling, goal, depth_limit - 1)
                if result and result.is_goal_reached():
                    return result
    return None



def generate_child_nodes(current_node, goal):
    new_queries = generate_new_queries(goal, current_node.get_context())
    child_nodes = []
    for query in new_queries:
        query_result, metadata, contexts = get_rag_response(query, languageBool=True)
        for context in contexts:
            confidence = evaluate_confidence_level(context, goal)
            child_node = current_node.add_child(query, context, confidence)
            child_nodes.append(child_node)
    return child_nodes

