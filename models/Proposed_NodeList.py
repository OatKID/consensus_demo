from models.Proposed_Node import Proposed_Node
from models.Role import Role
import random

class Proposed_NodeList:
    def __init__(self, num_master:int, num_slave:int, num_faulty:int=0) -> None:
        self.nodelist = self.generate_nodes(num_master, num_slave, num_faulty)
        self.node_filter = []
    
    def generate_nodes(self, num_master:int, num_slave:int, num_faulty:int):
        new_nodes = []
        try:
            if num_master + num_slave <= num_faulty:
                raise ValueError("the number of management and voting nodes are more than or equal to the number of faulty nodes")
            
            # * Make the management nodes
            for i in range(num_master):
                new_node = Proposed_Node(i, role=Role.MASTER)
                new_nodes.append(new_node)
            
            # * Make the voting node
            for i in range(num_master, num_master+num_slave):
                new_node = Proposed_Node(i, role=Role.SLAVE)
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

    def find_node(self, idUser:int) -> Proposed_Node:
        for node in self.nodelist:
            if node.idUser == idUser:
                return node
        return None

    def create_message(self, idUser:int, message:tuple, phase:str):
        current_node = self.find_node(idUser)
        current_node.create_message(message[0], phase)
    
    def get_all_nodes(self, role:Role=None, filter=False, include_faulty=True) -> list[Proposed_Node]:
        if role == None:
            if filter == False:
                return self.nodelist
            else:
                return self.node_filter
        
        filter_node = []
        if filter == False:
            nodelist = self.nodelist
        else:
            nodelist = self.node_filter
        
        for node in nodelist:
            if include_faulty == True:
                if node.role.value == role.value:
                    filter_node.append(node)
            else:
                if node.role.value == role.value and node.faulty == False:
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
    
    def get_num_nodes(self, role:Role=None, filter=False):
        if role == None:
            if filter == False:
                return len(self.nodelist)
            else:
                return len(self.node_filter)
        else:
            if filter == False:
                return len(self.get_all_nodes(role))
            else:
                return len(self.get_all_nodes(role, filter=True))
    
    def clear_messages_all_nodes(self):
        for current_node in self.nodelist:
            current_node.clear_all_messages()
    
    def random_faulty(self, num_fualty:int):
        for node in self.nodelist:
            node.faulty = False
        
        faulty_nodes = random.sample(self.nodelist, k=num_fualty)

        for f_node in faulty_nodes:
            f_node.faulty = True
    
    def clear_node_filter(self):
        self.node_filter.clear()