from models.QPBFT_Node import QPBFT_Node
import random
from Role import Role

class QPBFT_NodeList:
    def __init__(self, num_manager, num_voter, num_faulty, num_malicious) -> None:
        self.nodelist = self.generate_nodes(num_manager, num_voter, num_faulty, num_malicious)
    
    def generate_nodes(num_manager, num_voter, num_faulty, num_malicious):
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
            
            # * Random to select voting nodes to be malicious nodes
            if num_malicious > 0:
                malicious_nodes = random.sample(new_nodes[1:], k=num_malicious)
                for h_node in malicious_nodes:
                    h_node.is_mlicious = True

            return new_nodes

        except ValueError as e:
            print(e)
            return []
