# import sys
# import os

# path = os.getcwd()
# parent_path = os.path.abspath(os.path.join(path, os.pardir))
# sys.path.insert(0, f"{parent_path}")


from models.Node import Node
import random
from datetime import datetime
class PBFT_Simulator:
    def __init__(self, num_node:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = self.generate_nodes(num_node)
        
    
    def generate_nodes(self, num_node:int):
        new_nodes = []
        for i in range(num_node):
            new_node = {
                "node" : Node(i, str(datetime.now())),
                "send_messages_log": [],
                "receive_messages_log": [],
                "faulty": False
            }

            new_nodes.append(new_node)

        if self.num_faulty == 0:
            return new_nodes
    
        faulty_nodes = random.sample(new_nodes, k=self.num_faulty)
        for f_node in faulty_nodes:
            f_node["faulty"] = True
        return new_nodes

    def receive_request(self, message):
        # Let choose the leader node to receive a request by using index
        self.primary_node_index = random.randint(0, len(self.nodes)-1)
        while self.nodes[self.primary_node_index]["faulty"]:
            self.primary_node_index = random.randint(0, len(self.nodes)-1)
        
        recieve_message = (message, "request", -1) # -1 define to be the client which send a request
        self.nodes[self.primary_node_index]["receive_messages_log"].append(recieve_message)
    
    def broadcast_pre_prepare(self):
        message = self.nodes[self.primary_node_index]["receive_messages_log"][-1][0]
        pre_prepare_message = (message, "pre_preprare", self.primary_node_index)
        self.nodes[self.primary_node_index]["send_messages_log"].append(pre_prepare_message)

        for i in range(len(self.nodes)):
            if i != self.primary_node_index:
                self.receive_pre_prepare(pre_prepare_message, i)
    
    def receive_pre_prepare(self, message, index):
        self.nodes[index]["receive_messages_log"].append(message)
    
    def broadcast_prepare(self, current_node):
        message = current_node["receive_messages_log"][-1][0]
        prepare_message = (message, "prepare", current_node["node"].idUser)
        current_node["send_messages_log"].append(prepare_message)
        for i in range(len(self.nodes)):
            if (self.nodes[i] != current_node):
                self.receive_prepare(prepare_message, i)
    
    def receive_prepare(self, message, index):
        self.nodes[index]["receive_messages_log"].append(message)
        
    
    def get_nodes(self):
        for i in range(len(self.nodes)):
            print(self.nodes[i])
        print("-"*30)
    
    def send_request(self, new_transaction:str):

        # Start to recieve a request from the client
        print("Request Phase")
        self.receive_request(new_transaction)
        self.get_nodes()

        # The leader node broadcasts to the other nodes (Pre-Prepare Phase)
        print("Pre-Prepare Phase")
        self.broadcast_pre_prepare()
        self.get_nodes()

        # Other nodes which exclude the leader node will broadcast other nodes (Prepare Phase)
        print("Prepare Phase")
        for node in self.nodes:
            if node != self.nodes[self.primary_node_index] and (node["faulty"] == False):
                self.broadcast_prepare(node)
        self.get_nodes()

        # After each node have received prepare messages already, it will broadcast commit messages to make new block (Assume that the message is true)
