from models.QPBFT_Node import QPBFT_Node
from models.Role import Role
from datetime import datetime
from models.QPBFT_NodeList import QPBFT_NodeList
import random
class QPBFT_Simulator:
    def __init__(self, num_management:int, num_vote:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = QPBFT_NodeList(num_management, num_vote, num_faulty)
        self.primary_node:QPBFT_Node = None
        self.num_management = num_management
        self.num_vote = num_vote
        self.success_proof = 0
    
    def receive_request(self, message:str):
        if self.primary_node == None:
            self.primary_node = self.nodes.find_node(0)
        else:
            while self.primary_node.faulty:
                self.primary_node = random.sample(self.nodes.get_all_nodes(Role.MANAGER))
        
        self.primary_node.create_message(message, "prepare")
        self.primary_node.receive_message(self.primary_node.send_message_log)
    

    def boradcast_prepare(self):
        for current_node in self.nodes.get_all_nodes():
            if current_node != self.primary_node and current_node.role.value == "Voter":
                self.nodes.send_message(self.primary_node.idUser, current_node.idUser)
        
    
    def send_confirm_messages(self):
        # * Verfity messages whelter is not tampered and send it to the primary node.
        print([node.idUser for node in self.nodes.get_all_nodes(Role.VOTER)])
        for voting_node in self.nodes.get_all_nodes(Role.VOTER):
            if voting_node.verify_own_message("prepare") and voting_node.faulty != True:
                self.nodes.create_message(voting_node.idUser, voting_node.get_own_message("prepare"), "confirm")
                self.nodes.send_message(voting_node.idUser, self.primary_node.idUser)
    
    def verify_confirm_messages(self) -> bool:
        
        if self.primary_node.compare_phase("prepare", "confirm") and self.primary_node.get_num_messages_phase("confirm") >= 1 + (self.nodes.get_num_nodes(Role.VOTER)//2):
            return True
        else:
            return False
        
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

        print("Confirm Phase")
        self.send_confirm_messages()
        self.print_nodes()

        print("Generate-Block Phase")
        if self.verify_confirm_messages():
            print("Successful")
            self.success_proof += 1
        else:
            print("Fail")
        
        self.nodes.clear_messages_all_nodes()