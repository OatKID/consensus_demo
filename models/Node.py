from models.Blockchain import Blockchain
import secrets, hashlib
class Node:
    def __init__(self, idUser:int, faulty:bool=False) -> None:
        self.idUser = idUser
        self.blockchain = Blockchain()
        self.send_message_log = ""
        self.receive_messages_log = []
        self.faulty = faulty
        self.signature = secrets.token_urlsafe(16)
    
    def add_block(self, transaction:str, timestamp:str):
        return self.blockchain.add_block(transaction, timestamp)

    def __repr__(self) -> str:
        return f"IdUser => {self.idUser}, Faulty => {str(self.faulty):<5}, Send_messages => {str(self.send_message_log if self.send_message_log else "\'\'"):<35}, Receive_messages => {self.receive_messages_log}"

    def clear_messages(self):
        self.send_message_log = ""
        self.receive_messages_log.clear()
    
    def filter_messages(self, phase:str):
        new_messages = []
        for message in self.receive_messages_log:
            if message[1] == phase:
                new_messages.append(message)
        return new_messages
    
    def create_message(self, message:str, phase:str):
        new_message = (message, phase, self.idUser, hashlib.sha256(f"{message} {phase} {self.idUser}".encode()).hexdigest())
        self.send_message_log = new_message
    
    def receive_message(self, message:tuple):
        self.receive_messages_log.append(message)
    
    def verify_own_message(self, phase:str) -> bool:
        flag = True
        messages = self.filter_messages(phase)
        for message in messages:
            if message[3] != hashlib.sha256(f"{message[0]} {message[1]} {message[2]}".encode()).hexdigest():
                flag = False
        return flag
    
    def get_own_message(self, phase:str) -> str:
        if self.verify_own_message(phase):
            return self.filter_messages(phase)[0][0]
        return None