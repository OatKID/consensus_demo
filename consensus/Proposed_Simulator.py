from models.Proposed_Node import Proposed_Node
from models.Role import Role
import random
class Proposed_Simulator:
    def __init__(self, num_master, num_slave, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = self.generate_nodes(num_master, num_slave)
        
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

    def send_request(self):
        pass

    def brocast_internal(self):
        pass

    def reply_internal(self):
        pass

    def brocast_new_block(self):
        pass