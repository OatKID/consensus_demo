from models.Node import Node
import random, datetime
from models.NodeList import NodeList
class PBFT_Simulator:
    def __init__(self, num_node:int, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = NodeList(num_node, num_faulty)
        self.primary_node:Node = None
        self.success_proof = 0
        self.view_number = 0
        self.sequence_number = 0

    def receive_request(self, message):
        # * Let choose the leader node to receive a request by using index
        primary_node_index = random.randint(0, self.nodes.get_num_nodes()-1)
        while self.nodes.find_node(primary_node_index).faulty:
            primary_node_index = random.randint(0, self.nodes.get_num_nodes()-1)
        self.primary_node = self.nodes.find_node(primary_node_index)

        # * The primay node receives request-message from the client
        rec_message = (message, "request", -1) # -1 define to be the client which send a request
        self.primary_node.receive_message(rec_message)
    
    def broadcast_pre_prepare(self):
        # * The primary node create pre-prepare message to broadcast
        message = self.primary_node.get_own_message("request")
        self.primary_node.create_message(message[0], "pre-prepare")
        for current_node in self.nodes.get_all_nodes():
            self.nodes.send_message(self.primary_node.idUser, current_node.idUser)
    
    def broadcast_prepare(self):
        for current_node in self.nodes.get_all_nodes():
            if (current_node.idUser != self.primary_node.idUser) and (current_node.faulty != True):
                message = current_node.get_own_message("pre-prepare")
                self.nodes.create_message(current_node.idUser, message, "prepare")
                for other_node in self.nodes.get_all_nodes():
                    if current_node != other_node:
                        self.nodes.send_message(current_node.idUser, other_node.idUser)
       
    def broadcast_commit(self):
        for current_node in self.nodes.get_all_nodes():
            if current_node.faulty != True:
                if (current_node.verify_own_message("pre-prepare") or current_node.verify_own_message("request")) and current_node.verify_own_message("prepare"):
                    message = current_node.get_own_message("prepare")
                    self.nodes.create_message(current_node.idUser, message, "commit")
                    for other_node in self.nodes.get_all_nodes():
                        if current_node != other_node:
                            self.nodes.send_message(current_node.idUser, other_node.idUser)
            else:
                continue
    
    # def receive_commit(self, message, index):
    #     self.nodes[index].receive_messages_log.append(message)
    
    # def reply_client(self, current_node):
    #     count = 0
    #     for message in current_node.receive_messages_log:
    #         if message[1] == "commit":
    #             if message[3]:
    #                 count += 1
        
    #     if count >= 2 * self.num_faulty + 1:
    #         return 1
    #     else:
    #         return 0
    
    def get_nodes(self):
        for i in range(self.nodes.get_num_nodes()):
            print(self.nodes.find_node(i))
        print("-"*30)
    
    def send_request(self, new_transaction:str):

        # * Start to recieve a request from the client
        print("Request Phase")
        self.receive_request(new_transaction)
        self.get_nodes()

        # * The leader node broadcasts to the other nodes (Pre-Prepare Phase)
        print("Pre-Prepare Phase")
        self.broadcast_pre_prepare()
        self.get_nodes()

        # * Other nodes which exclude the leader node will broadcast other nodes (Prepare Phase)
        print("Prepare Phase")
        self.broadcast_prepare()
        self.get_nodes()

        # # After each node have received prepare messages already, it will broadcast commit messages to make new block (Assume that the message is true)
        print("Commit Phase")
        self.broadcast_commit()
        self.nodes.remove_phase_all_nodes("prepare")
        self.nodes.remove_phase_all_nodes("pre-prepare")
        self.get_nodes()
        
        # # After each node have received commit messages already, it will verify those messages to create new block. and reply to the client.
        # print("Reply Phase")
        # num_reply_messages = 0
        # for node in self.nodes:
        #     if node.faulty == False:
        #         num_reply_messages += self.reply_client(node)
        
        # if num_reply_messages >= self.num_faulty + 1:
        #     date = str(datetime.datetime.now())
        #     for node in self.nodes:
        #         if node.faulty == False:
        #             node.add_block(node.receive_messages_log[-1][0], date)
        #     print("Successfully in consensus")
        #     self.success_proof += 1
        # else:
        #     print("Fail in consensus")
        
        # for node in self.nodes:
        #     node.clear_all_messages()
        