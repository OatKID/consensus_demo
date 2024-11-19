from models.QPBFT_Node import QPBFT_Node
from models.Role import Role
from datetime import datetime
from models.QPBFT_NodeList import QPBFT_NodeList
import random
class QPBFT_Simulator:
    def __init__(self, num_management:int, num_vote:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = QPBFT_NodeList(num_management, num_vote, num_faulty)
        self.primary_node:QPBFT_Node = self.nodes.find_node(0)
        self.num_management = num_management
        self.num_vote = num_vote
        self.success_proof = 0
    
    def receive_request(self, message:str):
        self.primary_node.create_message(message, "prepare")
        self.primary_node.receive_message(self.primary_node.send_message_log)
    

    def boradcast_prepare(self):
        for current_node in self.nodes.get_all_nodes():
            if current_node != self.primary_node and current_node.role.value == "Voter":
                self.nodes.send_message(self.primary_node.idUser, current_node.idUser)
        
        # * Verfity messages whelter is not tampered.
        for voting_node in self.nodes.get_all_nodes(Role.VOTER):
            if voting_node.verify_own_message("prepare") and voting_node.faulty != True:
                self.nodes.create_message(voting_node.idUser, voting_node.get_own_message("prepare"), "commit")
    
    def send_commit_message(self):
        pass

    def print_nodes(self):
        for i in range(self.nodes.get_num_nodes()):
            print(self.nodes.find_node(i))
        print("-"*30)
    
    def send_request(self, message:str):
        
        print("Request Phase")
        self.receive_request(message)
        self.print_nodes()

        print("Prepare Phase")
        self.boradcast_prepare()
        self.print_nodes()

        print("Commit Phase")

        print("Generate-Block Phase")