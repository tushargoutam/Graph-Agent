import asyncio
from logger import logger

class WorkFlowEngine():

    """
    WorkFlow Engine: This is a class that consist of Four basic elements. And this is used to create or define any automated Pipeline.
    1. Nodes
    2. Edges
    3. Conditions
    4. State

    and there are functions to help with the workflow and to create workflow
    where 
        Nodes : These are a autonomous blocks that are specialized for a certain task
        Edges : These are the the Direction and path from One node to another, Basically Defining 
                the pipeline.
        State: States is a term here that is given to define the current position of the process. 
                At what step the process is on.
        Condition: This is basically a check to control the quality or some condition before proceeding
                    from one state to another
    """
    def __init__(self):

        """
        Docstring for __init__

        This is a constructor method to define variables for the class object.
        
        :param self: For mapping to the object of this class self is replaced by object names and then any method or variable assciated with the class can be accessed.

        """

        # Dictonary to contain the created Node
        self.nodes = {}

        # Dictonary to contain the edges(paths)
        self.edges = {}

        # Dictonary to Register any condition if applicable.
        self.conditions = {}

    def add_node(self,name,func):
        """
        Docstring for add_node

        This method is used to add a node to the system
        
        :param self: Placeholder for the class object
        :param name: Name of the Node
        :param func: Working of node defined as a function(set of operations)
        """

        self.nodes[name] = func

    def add_edge(self, start_node,end_node):
        """
        Docstring for add_edge

        This method is used to create a pipeline or direction from one edge to another.
        
        :param self: Place holder for the object
        :param start_node: Node from where the edge starts 
        :param end_node: Node where the edge points to
        """
        self.edges[start_node] = end_node

    def add_condition(self,start_node,condition_function):
        """
        Docstring for add_condition

        This method is used give anycondition that needs to be satisfied in one node before moving on to next node
        
        :param self: Place holder for the object.
        :param start_node: Which Node the condition should be applied on.
        :param condition_function : Condition you want to apply on the current node.
        """
        self.conditions[start_node] = condition_function


    async def run(self,start_node, initial_state):
        """
        Docstring for run

        This function 
        
        :param self: Place holder for the object.
        :param start_node: Which node to start from.
        :param initial_state: What is the intial state according to node.
        """

        current_node = start_node
        state = initial_state

        logger.info(f"Starting the Workflow at: {start_node}")

        while current_node:
            if current_node not in self.nodes:
                logger.error(f"Error: Node '{current_node}' is not recognised as a registerd Node. Please Register the node.")
                break

            node_func = self.nodes[current_node]
            try:
                state = await node_func(state)
                logger.info(f"Ececuted Node: {current_node}")
            except Exception as e:
                logger.error(f"Error while executing {current_node} : {e}")
                break


            next_node = None 
            
            if current_node in self.conditions:
                condition_func = self.conditions[current_node]
                next_node = condition_func(state)
            elif current_node in self.edges:
                next_node = self.edges[current_node]

            current_node = next_node

        logger.info("Workflow Finished")
        return state
