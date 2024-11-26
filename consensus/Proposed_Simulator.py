from models.Proposed_Node import Proposed_Node
from models.Proposed_NodeList import Proposed_NodeList
from models.Role import Role
import random
from datetime import datetime
class Proposed_Simulator:
    def __init__(self, num_master:int, num_slave:int, k:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.num_proposed_nodes = k
        self.nodes = Proposed_NodeList(num_master, num_slave, num_faulty)
        self.primary_node = None
        self.success_proof = 0
    
    def select_primary_node(self):
        self.nodes.normalize_priority()
        node_filter = self.nodes.get_all_nodes(filter=True)
        sorted(node_filter, key=lambda node: node.priority)
        for node in node_filter:
            if node.faulty == False:
                self.primary_node = node
                break
    
    def print_nodes(self, filter=False):
        for node in self.nodes.get_all_nodes(filter=filter):
            print(node)
        print("-"*30)

    def receive_request(self, message:str):

        self.nodes.select_nodes_consensus(self.num_proposed_nodes)
        self.select_primary_node()
        self.primary_node.receive_message((message, "request", -1))
        self.primary_node.create_message(message, "prepare")

    def send_request(self, request:str):
        
        # The client sends a request to proposed_nodes which there is a the primary node to receive a request.
        print("Request Phase")
        self.receive_request(request)
        self.print_nodes()
