from models.QPBFT_Node import QPBFT_Node
from models.Role import Role
from datetime import datetime
from models.QPBFT_NodeList import QPBFT_NodeList
import random
class QPBFT_Simulator:
    def __init__(self, num_management:int, num_vote:int, num_faulty:int=0, malicious:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = QPBFT_NodeList(num_management, num_vote, num_faulty, malicious)
        self.primary_node = self.nodes[0]
        self.num_management = num_management
        self.num_vote = num_vote
        self.success_proof = 0
    
    def receive_request(self, message:str):
        pass
    
    def send_request(self, message:str):
        
        print("Request Phase")

        print("Prepare Phase")

        print("Commit Phase")

        print("Generate-Block Phase")