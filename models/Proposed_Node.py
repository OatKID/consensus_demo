from models.Node import Node
from models.Role import Role
import random
class Proposed_Node(Node):
    def __init__(self, idUser: int, faulty: bool = False, role:Role=Role.SLAVE) -> None:
        super().__init__(idUser, faulty)
        self.role = role
        self.priority = random.randint(0, 100)
    
    def __repr__(self) -> str:
        return f"IdUser => {self.idUser}, Role => {self.role.value:>7}, send_message_log => {str(self.send_message_log if self.send_message_log else "\'\'"):<35}, messages_log => {self.messages_log}"

    

