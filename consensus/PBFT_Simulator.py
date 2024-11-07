# import sys
# import os

# path = os.getcwd()
# parent_path = os.path.abspath(os.path.join(path, os.pardir))
# sys.path.insert(0, f"{parent_path}")


from models.Node import Node
import random
class PBFT_Simulator:
    def __init__(self, num_node:int) -> None:
        self.nodes = self.generate_nodes(num_node)
    
    def generate_nodes(self, num_node:int):
        new_nodes = []
        for i in range(num_node):
            new_node = {
                "node" : Node(i, random.randint(0, 10)),
                "messages_log": [],
            }

            new_nodes.append(new_node)
        return new_nodes

    def run(self, new_transaction:str):
        
        # Let choose the leader node to receive a request by using index
        primary_node_index = random.randint(0, len(self.nodes)-1)

        # Start to recieve a request from the client
        self.receive_request(new_transaction, primary_node_index)
        self.get_nodes()

        # The leader node broadcasts to the other nodes (Pre-Prepare phase)
        self.broadcast_pre_prepare(primary_node_index)
        self.get_nodes()
    
    def receive_request(self, message, primary_node_index):
        pre_prepare_message = (message, "pre-prepare")
        self.nodes[primary_node_index]["messages_log"].append(pre_prepare_message)
    
    def broadcast_pre_prepare(self, primary_node_index):
        message = self.nodes[primary_node_index]["messages_log"][-1][0]
        for i in range(len(self.nodes)):
            if i != primary_node_index:
                self.receive_pre_prepare(message, i)
    
    def receive_pre_prepare(self, message, index):
        prepare_message = (message, "prepare")
        self.nodes[index]["messages_log"].append(prepare_message)
    
    def get_nodes(self):
        for i in range(len(self.nodes)):
            print(self.nodes[i])
        print("-"*30)

