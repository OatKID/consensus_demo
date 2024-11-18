from models.QPBFT_Node import QPBFT_Node
from models.Role import Role
from datetime import datetime
import random
class QPBFT_Simulator:
    def __init__(self, num_management:int, num_vote:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = self.generate_nodes(num_management, num_vote)
        self.primary_node_index = 0
        self.num_management = num_management
        self.num_vote = num_vote
        self.success_proof = 0
    
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
    
    def broadcast_prepare(self):
        message = self.nodes[self.primary_node_index].messages_log[-1]
        prepare_message = (message[0], "prepare", self.nodes[self.primary_node_index].idUser)
        self.nodes[self.primary_node_index].send_message_log = prepare_message

        for current_node in self.nodes:
            if current_node.role.value == Role.VOTER.value:
                self.receive_prepare(current_node, prepare_message)

    def receive_prepare(self, node, prepare_message):
        node.messages_log.append(prepare_message)

    
    def reply_management(self):
        for current_node in self.nodes:
            if (current_node.role.value == Role.VOTER.value) and (current_node.faulty == False):
                message = current_node.messages_log[-1]
                confirm = random.randint(0, 1)
                confirm_message = (message[0], "confirm", current_node.idUser, confirm)
                current_node.send_message_log = confirm_message
                self.nodes[self.primary_node_index].messages_log.append(confirm_message)
    
    def get_user_receive(self, n):
        return n[2]

    def sort(self, list_of_tuples):
        return sorted(list_of_tuples, key=self.get_user_receive)
    
    def verfity_vote(self):
        messages = self.sort(self.nodes[self.primary_node_index].messages_log)
        messages = messages[1:]
        
        count_vote = 0
        for message in messages:
            if message[3]:
                count_vote += 1

        if count_vote >= 1 + (self.num_vote//2):
            return True
        else:
            return False
        
    def broadcast_new_block(self):
        message = self.nodes[self.primary_node_index].send_message_log[0]
        for node in self.nodes:
            if node.faulty == False:
                node.add_block(message, datetime.now())
    
    def print_nodes(self):
        for i in range(len(self.nodes)):
            print(self.nodes[i])
        print("-"*30)
    
    def send_request(self, request:str):
        # The client begins to send a request to the management node which is selected to receive.
        print("Request Phase")
        self.nodes[self.primary_node_index].messages_log.append((request, "request", -1))
        self.print_nodes()

        # The management node broadcasts a prepare-message to voting nodes
        print("Prepare Phase")
        self.broadcast_prepare()
        self.print_nodes()

        # The voting nodes commit the message and reply a commit-message to the management node
        print("Commit Phase")
        self.reply_management()
        self.print_nodes()

        # The management node verify the number of votes, which are accepted a message, to create management.
        print("Produce Block Phase")
        if self.verfity_vote():
            self.broadcast_new_block()
            print("Complete")
            self.success_proof += 1
        else:
            print("Fail")
        
        checkFaulty = True
        while checkFaulty:
            self.primary_node_index = random.randint(0, self.num_management + self.num_vote - 1)
            current_node = self.nodes[self.primary_node_index]
            if (current_node.faulty == False) and (current_node.role.value == Role.MANAGER.value):
                checkFaulty = False
                break
        
        for node in self.nodes:
            node.clear_all_messages()
        