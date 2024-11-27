from models.Node import Node
from models.Role import Role
import random
class Proposed_Node(Node):
    def __init__(self, idUser: int, faulty: bool = False, role:Role=Role.SLAVE) -> None:
        super().__init__(idUser, faulty)
        self.role = role
        self.priority = random.randint(0, 100)
    
    def __repr__(self) -> str:
        return f"IdUser => {self.idUser}, Priority => {self.priority:.2f}, Role => {self.role.value:>7}, Faulty => {str(self.faulty):>6}, Send_Message => {str(self.send_message_log[0:3] if self.send_message_log else "\'\'"):<35}, Messages_Log => {self.messages_log}"

    

