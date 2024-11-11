from models.Blockchain import Blockchain
class Node:
    def __init__(self, idUser:int, faulty:bool=False, role:str=None) -> None:
        self.idUser = idUser
        self.blockchain = Blockchain()
        self.send_messages_log = ""
        self.receive_messages_log = []
        self.faulty = faulty
        self.role = role
    
    def add_block(self, transaction:str, timestamp:str):
        return self.blockchain.add_block(transaction, timestamp)

    def __repr__(self) -> str:
        return f"IdUser => {self.idUser}, Faulty => {str(self.faulty):<5}, Send_messages => {str(self.send_messages_log if self.send_messages_log else "\'\'"):<35}, Receive_messages => {self.receive_messages_log}"