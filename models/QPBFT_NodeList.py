from models.QPBFT_Node import QPBFT_Node
import random
from models.Role import Role
import numpy
class QPBFT_NodeList:
    def __init__(self, num_manager, num_voter, num_faulty) -> None:
        self.nodelist = self.generate_nodes(num_manager, num_voter, num_faulty)
        self.node_filter = []
    
    def generate_nodes(self, num_manager, num_voter, num_faulty):
        new_nodes = []
        try:
            if num_manager + num_voter <= num_faulty:
                raise ValueError("the number of management and voting nodes are more than or equal to the number of faulty nodes")
            
            # * Make the management nodes
            for i in range(num_manager):
                new_node = QPBFT_Node(i, role=Role.MANAGER)
                new_nodes.append(new_node)
            
            # * Make the voting node
            for i in range(num_manager, num_manager+num_voter):
                new_node = QPBFT_Node(i, role=Role.VOTER)
                new_nodes.append(new_node)
            
            # * Random to select nodes to be faulty nodes
            if num_faulty > 0:
                faulty_nodes = random.sample(new_nodes[1:], k=num_faulty)
            
                for f_node in faulty_nodes:
                    f_node.faulty = True

            return new_nodes

        except ValueError as e:
            print(e)
            return []
    
    def find_node(self, idUser:int) -> QPBFT_Node:
        for node in self.nodelist:
            if node.idUser == idUser:
                return node
        return None

    def create_message(self, idUser:int, message:tuple, phase:str):
        current_node = self.find_node(idUser)
        current_node.create_message(message[0], phase)
    
    def get_all_nodes(self, role:Role=None) -> list[QPBFT_Node]:
        if role == None:
            return self.nodelist

        filter_node = []
        for node in self.nodelist:
            if node.role.value == role.value:
                filter_node.append(node)
        
        return filter_node

    def send_message(self, origin_node_idUser:int, destination_node_idUser:int) -> bool:
        origin_node = self.find_node(origin_node_idUser)
        destination_node = self.find_node(destination_node_idUser)

        if origin_node.faulty != True:
            message = origin_node.send_message_log
            self.receive_message(destination_node.idUser, message)
            return True
        else:
            return False
    
    def receive_message(self, idUser:int, message_form:tuple):
        current_node = self.find_node(idUser)
        current_node.receive_message(message_form)
    
    def get_num_nodes(self, role:Role=None):
        if role == None:
            return len(self.nodelist)
        else:
            return len(self.get_all_nodes(Role.VOTER))
    
    def clear_messages_all_nodes(self):
        for current_node in self.nodelist:
            current_node.clear_all_messages()
    
    def calcuate_reliable_score(self):
        weight = numpy.array([0.0675, 0.2521, 0.3743, 0.0631, 0.0072, 0.0197])
        scores = numpy.array([])
        for node in self.nodelist:
            node_reliability_score = numpy.array(node.generate_score())
            score = numpy.dot(weight, node_reliability_score)
            scores = numpy.append(scores, score)
        
        min_score = numpy.min(scores)
        max_score = numpy.max(scores)

        differenct = max_score - min_score
        for i in range(self.get_num_nodes()):
            normalized_score = (scores[i] - min_score)/differenct
            node:QPBFT_Node = self.nodelist[i]
            node.set_relibable_score(normalized_score)
            
    # def filter_node(self):
    #     self.calcuate_reliable_score()
    
    # * Set faulty node in each next round
    def random_faulty(self, num_fualty:int):
        for node in self.nodelist:
            node.faulty = False
        
        faulty_nodes = random.sample(self.nodelist, k=num_fualty)

        for f_node in faulty_nodes:
            f_node.faulty = True