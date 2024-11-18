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
        return f"IdUser => {self.idUser}, Faulty => {str(self.faulty):<5}, Send_messages => {str(self.send_message_log[0:3] if self.send_message_log else "\'\'"):<35}, Receive_messages => {self.receive_messages_log}"

    def clear_all_messages(self):
        self.send_message_log = ""
        self.receive_messages_log.clear()
    
    def remove_phase(self, phase:str):
        messages = self.filter_messages(phase)
        for message in messages:
            self.receive_messages_log.remove(message)

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

        if phase == "request":
            message = self.receive_messages_log[0]
            if message[1] == "request":
                return True
            else:
                return False

        flag = True
        messages = self.filter_messages(phase)
        for message in messages:
            if message[3] != hashlib.sha256(f"{message[0]} {message[1]} {message[2]}".encode()).hexdigest():
                flag = False
        return flag

    def compare_phase(self, phase1:str, phase2:str):
        message1 = self.filter_messages(phase1)
        message2 = self.filter_messages(phase2)

        if len(phase1) < len(phase2):
            temp = message1
            message1 = message2
            message2 = temp
        
        flag = True
        for check_message in message2:
            if check_message != message1:
                flag = False
                return flag
        return flag
        
    def get_own_message(self, phase:str) -> tuple:
        if self.verify_own_message(phase):
            messages = self.filter_messages(phase)[0]
            return messages
        return None