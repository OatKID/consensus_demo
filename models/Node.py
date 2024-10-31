from models.Blockchain import Blockchain
from models.Block import Block
class Node:
    def __init__(self, idUser:str, timestamp:str) -> None:
        self.idUser = idUser
        self.timestamp = timestamp
        self.blockchain = Blockchain()
        self.is_leader = False
    
    # Own node will create new block in own blockchain by having transaction and timestamp when block is created.
    def add_block(self, transaction:str, timestamp:str) -> Block:
        new_block = self.blockchain.add_block(transaction, timestamp)
        return new_block
    
    def __repr__(self) -> str:
        return f"{self.idUser} {self.timestamp} {self.is_leader} {self.blockchain}"
    
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