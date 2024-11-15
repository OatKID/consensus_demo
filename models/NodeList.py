from models.Node import Node
from models.QPBFT_Node import QPBFT_Node
from models.Proposed_Node import Proposed_Node
import random
import hashlib

class NodeList:
    def __init__(self, num_node:int, num_faulty:int) -> None:
        self.nodelist = self.generate_nodes(num_node, num_faulty)
    
    def generate_nodes(self, num_node:int, num_faulty:int):
        new_nodes = []
        try:
            if num_node <= num_faulty:
                raise ValueError("Error: The number of nodes is more than the number of faulty nodes.")
            for i in range(num_node):
                new_node = Node(i)
                new_nodes.append(new_node)

            if num_faulty > 0:
                faulty_nodes = random.sample(new_nodes, k=num_faulty)
                for f_node in faulty_nodes:
                    f_node.faulty = True
            
            return new_nodes

        except ValueError as e:
            print(e)
            return False
     
    def create_message(self, idUser:int, message:tuple, phase:str):
        current_node = self.find_node(idUser)
        current_node.create_message(message[0], phase)
    
    def send_message(self, origin_node_idUser:int, destination_node_idUser:int) -> bool:
        origin_node = self.find_node(origin_node_idUser)
        destination_node = self.find_node(destination_node_idUser)

        if origin_node.faulty != True:
            message = origin_node.send_message_log
            self.receive_message(destination_node.idUser, message)
            return True
        else:
            return False
    
    def receive_message(self, idUser:int, message_form:tuple):
        current_node = self.find_node(idUser)
        current_node.receive_message(message_form)
    
    def find_node(self, idUser:int) -> Node:
        for node in self.nodelist:
            if node.idUser == idUser:
                return node
        return None

    def get_num_nodes(self):
        return len(self.nodelist)

    def get_all_nodes(self):
        return self.nodelist