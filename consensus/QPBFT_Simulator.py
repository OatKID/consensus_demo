from models.QPBFT_Node import QPBFT_Node
from models.Role import Role
from datetime import datetime
import random
class QPBFT_Simulator:
    def __init__(self, num_management:int, num_vote:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = self.generate_nodes(num_management, num_vote)
        self.primary_node = None
        self.num_management = num_management
        self.num_vote = num_vote
        self.success_proof = 0
    
    
    
    def send_request(self, message:str):
        pass