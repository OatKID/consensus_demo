from models.QPBFT_Node import QPBFT_Node
from models.Role import Role
from datetime import datetime
import random
class QPBFT_Simulator:
    def __init__(self, num_management:int, num_vote:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = self.generate_nodes(num_management, num_vote)
    
    def generate_nodes(self, num_management, num_vote):
        new_nodes = []
        for i in range(num_management):
            new_node = QPBFT_Node(i, role=Role.MANAGER)
            new_nodes.append(new_node)
        
        for i in range(num_management, num_management + num_vote):
            new_node = QPBFT_Node(i, role=Role.VOTER)
            new_nodes.append(new_node)
        
        faulty_nodes = random.sample(new_nodes, k=self.num_faulty)
        for f_node in faulty_nodes:
            f_node.faulty = True

        return new_nodes
    
    def brocastcast(self):
        pass
    
    def reply_management(self):
        pass
    
    
    def send_request(self, request:str):
        pass
    