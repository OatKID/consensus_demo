from models.Node import Node
import random, datetime
from models.NodeList import NodeList
class PBFT_Simulator:
    def __init__(self, num_nodes:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = NodeList(num_nodes, num_faulty)
        self.primary_node:Node = None
        self.success_proof = 0
        self.view_number = 0
        self.num_nodes = num_nodes
        # self.sequence_number = 0


    def receive_request(self, message):
        # * Let choose the leader node to receive a request by using index
        primary_node_index = self.view_number % self.num_nodes
        while self.nodes.nodelist[primary_node_index].faulty == True:
            self.view_number += 1
            primary_node_index = self.view_number % self.num_nodes

        self.primary_node = self.nodes.nodelist[primary_node_index]

        # * The primary node receive the request and make a pre-prepare message to insert its log.
        self.primary_node.create_message(message, "pre-prepare")
        self.primary_node.receive_message(self.primary_node.send_message_log)
    
    # * The primary node create pre-prepare message to broadcast the backup node
    def broadcast_pre_prepare(self):
        for current_node in self.nodes.get_all_nodes():
            if current_node != self.primary_node:
                self.nodes.send_message(self.primary_node.idUser, current_node.idUser)
        
        # * Verify pre-prepare message to make prepare message
        for current_node in self.nodes.get_all_nodes():
            if current_node.verify_own_message("pre-prepare") and current_node.faulty != True:
                self.nodes.create_message(current_node.idUser, current_node.get_own_message("pre-prepare"), "prepare")
    
    def broadcast_prepare(self):
        for current_node in self.nodes.get_all_nodes():
            if current_node != self.primary_node and current_node.faulty != True:
                for other_node in self.nodes.get_all_nodes():
                    if current_node != other_node:
                        self.nodes.send_message(current_node.idUser, other_node.idUser)
                    else:
                        pass
            else:
                pass
        
        # * Verify prepare message to make commit message
        for current_node in self.nodes.get_all_nodes():
            if self.verify_prepare(current_node) and current_node.faulty != True:
                self.nodes.create_message(current_node.idUser, current_node.get_own_message("prepare"), "commit")

    def verify_prepare(self, current_node:Node) -> bool:
        if current_node.verify_own_message("prepare") and current_node.compare_phase("pre-prepare", "prepare") and (current_node.get_num_messages_phase("prepare") >= 2 * self.num_faulty):
            return True
        else:
            return False
        
    
    def broadcast_commit(self):
        for current_node in self.nodes.get_all_nodes():
            if current_node.faulty != True:
                for other_node in self.nodes.get_all_nodes():
                    if current_node != other_node:
                        self.nodes.send_message(current_node.idUser, other_node.idUser)
                    else:
                        pass
            else:
                pass
                
        # * Verify commit messages to excute operation
        if self.verify_committed_local() and self.verify_committed():
            print("Successful")
            self.success_proof += 1
            message = self.primary_node.get_own_message("pre-prepare")
            timestamp = str(datetime.datetime.now())
            for node in self.nodes.get_all_nodes():
                node.add_block(message, timestamp)
        else:
            print("Fail")
    
    def verify_committed(self) -> bool:
        count_replica = 0 # Count replicas whose verify prepared to be true
        for current_node in self.nodes.get_all_nodes():
            if self.verify_prepare(current_node) and current_node.faulty != True:
                count_replica += 1
        
        if count_replica > self.num_faulty + 1:
            return True
        else:
            return False
            
    def verify_committed_local(self) -> bool:
        for current_node in self.nodes.get_all_nodes():
            if self.verify_prepare(current_node) and current_node.get_num_messages_phase("commit") >= 2*self.num_faulty + 1 and current_node.faulty != True:
                return True
        return False
    
    def print_nodes(self):
        for i in range(self.nodes.get_num_nodes()):
            print(self.nodes.find_node(i))
        print("-"*30)
    
    def send_request(self, new_transaction:str):

        # * Start to recieve a request from the client
        # //print("Request Phase")
        self.receive_request(new_transaction)
        # //self.print_nodes()

        # * The leader node broadcasts to the other nodes (Pre-Prepare Phase)
        # //print("Pre-Prepare Phase")
        self.broadcast_pre_prepare()
        # //self.print_nodes()

        # * Other nodes which exclude the leader node will broadcast other nodes (Prepare Phase)
        # //print("Prepare Phase")
        self.broadcast_prepare()
        # //self.print_nodes()

        # * After each node have received prepare messages already, it will broadcast commit messages to make new block (Assume that the message is true)
        # //print("Commit Phase")
        self.broadcast_commit()
        # //self.print_nodes()
        
        self.nodes.clear_messages_all_nodes()
        self.nodes.random_faulty(self.num_faulty)
        self.view_number += 1
        
        