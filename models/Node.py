from models.Blockchain import Blockchain
class Node:
    def __init__(self, idUser:int, timestamp:str) -> None:
        self.idUser = idUser
        self.timestamp = timestamp
        self.blockchain = Blockchain()
    
    def add_block(self, transaction:str, timestamp:str):
        return self.blockchain.add_block(transaction, timestamp)

    def __repr__(self) -> str:
        return f"IdUser=> {self.idUser}"