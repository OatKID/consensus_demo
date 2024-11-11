from models.Node import Node
from models.Role import Role
from datetime import datetime
import random
class QPBFT_Simulator:
    def __init__(self, num_management:int, num_vote:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.management_nodes = self.generate_nodes(num_management, Role.MANAGER)
        self.vote_nodes = self.generate_nodes(num_management, Role.VOTER)
    
    def generate_nodes(self, num_node, role:Role):
        new_nodes = []
        for i in range(num_node):
            new_node = Node(i, role=role)
            new_nodes.append(new_node)
        return new_nodes

    
    def brocastcast(self):
        pass
    
    def reply_management(self):
        pass
    
    
    def send_request(self, request:str):
        pass
    