from models.Proposed_Node import Proposed_Node
from models.Role import Role
import random
from datetime import datetime
class Proposed_Simulator:
    def __init__(self, num_master:int, num_slave:int, k:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.num_proposed_nodes = k
        self.nodes = self.generate_nodes(num_master, num_slave)
        self.proposed_nodes = random.sample(self.nodes, k=k)
        self.primary_node_index = self.select_primary_node()
        
    def generate_nodes(self, num_master, num_slave):
        new_nodes = []
        for i in range(num_master):
            new_node = Proposed_Node(i, role=Role.MASTER)
            new_nodes.append(new_node)
        
        for i in range(num_master, num_master+num_slave):
            new_node = Proposed_Node(i, role=Role.SLAVE)
            new_nodes.append(new_node)
        
        faulty_nodes = random.sample(new_nodes, k=self.num_faulty)
        for f_node in faulty_nodes:
            f_node.faulty = True
        
        return new_nodes
    
    def print_nodes(self, nodes):
        for node in nodes:
            print(node)
        print("-"*30)
    
    def select_primary_node(self):
        primary_node_index = 0
        max_priority = 0
        for i in range(len(self.proposed_nodes)):
            if self.proposed_nodes[i].priority > max_priority:
                primary_node_index = i
                max_priority = self.proposed_nodes[i].priority
        return primary_node_index
    
    def broadcast_internal(self):
        message = self.proposed_nodes[self.primary_node_index].receive_messages_log[-1][0]
        prepare_message = (message, "prepare", self.proposed_nodes[self.primary_node_index].idUser)
        self.proposed_nodes[self.primary_node_index].send_messages_log = prepare_message
        for node in self.proposed_nodes:
            if node.idUser != self.proposed_nodes[self.primary_node_index].idUser:
                self.receive_prepare(node, prepare_message)
    
    def receive_prepare(self, node, message):
        node.receive_messages_log.append(message)

    def reply_internal(self):
        for node in self.proposed_nodes:
            if node.idUser != self.proposed_nodes[self.primary_node_index].idUser:
                message = node.receive_messages_log[-1]
                vote = random.randint(0, 1)
                commit_message = (message[0], "commit", node.idUser, vote)
                node.send_messages_log = commit_message
                self.proposed_nodes[self.primary_node_index].receive_messages_log.append(commit_message)

    def verify_vote(self):
        messages = self.proposed_nodes[self.primary_node_index].receive_messages_log[1:]
        count_vote = 0
        for message in messages:
            if message[3]:
                count_vote += 1
        
        if count_vote >= (len(self.proposed_nodes) * 2)//3:
            return True
        else:
            return False

    def broadcast_new_block(self):
        message = self.proposed_nodes[self.primary_node_index].send_messages_log
        new_block_message = (message[0], "new_block", self.proposed_nodes[self.primary_node_index].idUser)
        for node in self.nodes:
            if node.faulty == False:
                self.receive_new_block(node, new_block_message)
        pass
    
    def receive_new_block(self, node, message):
        node.receive_messages_log.append(message)
        if node.role.value == Role.MASTER.value:
            timestamp = str(datetime.now())
            node.add_block(message[0], timestamp)

    def send_request(self, request:str):
        # The client sends a request to proposed_nodes which there is a the primary node to receive a request.
        self.proposed_nodes[self.primary_node_index].receive_messages_log.append((request, "request", -1))
        self.print_nodes(self.proposed_nodes)
        
        # The primary node broadcast a request to other nodes in the group of proposed nodes.
        self.broadcast_internal()
        self.print_nodes(self.proposed_nodes)

        # Each node in the proposed nodes reply the leader node a commit-message.
        self.reply_internal()
        self.print_nodes(self.proposed_nodes)

        # Verify the number of votes to make new block.
        if self.verify_vote():
            self.broadcast_new_block()
            self.print_nodes(self.nodes)
            print("Complete")
        else:
            print("Fail")
        
        # Choose proposed nodes to do consensus next round
        self.proposed_nodes = random.sample(self.nodes, k=self.num_proposed_nodes)
        self.primary_node_index = self.select_primary_node()