from models.Blockchain import Blockchain
class Node:
    def __init__(self, idUser:int, faulty:bool=False) -> None:
        self.idUser = idUser
        self.blockchain = Blockchain()
        self.send_messages_log = ""
        self.receive_messages_log = []
        self.faulty = faulty
    
    def add_block(self, transaction:str, timestamp:str):
        return self.blockchain.add_block(transaction, timestamp)

    def __repr__(self) -> str:
        return f"IdUser => {self.idUser}, Faulty => {str(self.faulty):<5}, Send_messages => {str(self.send_messages_log if self.send_messages_log else "\'\'"):<35}, Receive_messages => {self.receive_messages_log}"

    def clear_messages(self):
        self.send_messages_log = ""
        self.receive_messages_log.clear()
    
    def filter_messages(self, phase:str):
        new_messages = []
        for message in self.receive_messages_log:
            if message[1] == phase:
                new_messages.append(message)
        return new_messages