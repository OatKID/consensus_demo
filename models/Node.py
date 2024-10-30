from Blockchain import Blockchain
from Block import Block
class Node:
    def __init__(self, idUser:str, timestamp:str) -> None:
        self.idUser = idUser
        self.timestamp = timestamp
        self.blockchain = Blockchain()
        self.is_leader = False
    
    def add_block(self, transaction:str, timestamp:str) -> Block:
        new_block = self.blockchain.add_block(transaction, timestamp)
        return new_block
    
    def receive_request(self, messages:str):
        pass

    def receive_prepare(self, messages:str):
        pass

    def receive_decide(self, messages:str):
        pass

    def setLeader(self):
        self.is_leader = True
    
    def unsetLeader(self):
        self.is_leader = False