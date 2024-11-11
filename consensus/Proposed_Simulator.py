class Proposed_Simulator:
    def __init__(self, num_master, num_slave, num_faulty:int=0) -> None:
        self.num_faulty = num_faulty
        self.nodes = self.generate_nodes(num_master, num_slave, num_faulty)
        
    def generate_nodes(self, num_master, num_slave, num_faulty):
        pass

    def send_request(self):
        pass

    def brocast_internal(self):
        pass

    def reply_internal(self):
        pass

    def brocast_new_block(self):
        pass