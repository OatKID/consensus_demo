# import sys
# import os

# path = os.getcwd()
# parent_path = os.path.abspath(os.path.join(path, os.pardir))
# sys.path.insert(0, f"{parent_path}")


from models.Node import Node
import random
from datetime import datetime
class PBFT_Simulator:
    def __init__(self, num_node:int) -> None:
        self.nodes = self.generate_nodes(num_node)
        # Let choose the leader node to receive a request by using index
        self.primary_node_index = random.randint(0, len(self.nodes)-1)
    
    def generate_nodes(self, num_node:int):
        new_nodes = []
        for i in range(num_node):
            new_node = {
                "node" : Node(i, str(datetime.now())),
                "send_messages_log": [],
                "receive_messages_log": [],
            }

            new_nodes.append(new_node)
        return new_nodes

    def receive_request(self, message):
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
            if self.nodes[i] != current_node:
                self.receive_prepare(prepare_message, i)
    
    def receive_prepare(self, message, index):
        self.nodes[index]["receive_messages_log"].append(message)
        
    
    def get_nodes(self):
        for i in range(len(self.nodes)):
            print(self.nodes[i])
        print("-"*30)
    
    def send_request(self, new_transaction:str):

        # Start to recieve a request from the client
        self.receive_request(new_transaction)
        self.get_nodes()

        # The leader node broadcasts to the other nodes (Pre-Prepare phase)
        self.broadcast_pre_prepare()
        self.get_nodes()

        for node in self.nodes:
            if node != self.nodes[self.primary_node_index]:
                self.broadcast_prepare(node)
        
        self.get_nodes()

