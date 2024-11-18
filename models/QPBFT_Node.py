from models.Node import Node
from models.Role import Role
import random
class QPBFT_Node(Node):
    def __init__(self, idUser: int,faulty: bool = False, role:Role=Role.VOTER) -> None:
        super().__init__(idUser, faulty)
        self.role = role
        self.reliable_socre = 0
    
    def __repr__(self) -> str:
        return f"IdUser => {self.idUser}, Role => {self.role.value:>8}, Faulty => {str(self.faulty):>6}, send_message_log => {str(self.send_message_log if self.send_message_log else "\'\'"):<35}, messages_log => {self.messages_log}"
    
    def _generate_score(self, num_value):
        array = []
        for i in range(num_value):
            value = random.randint(0, 100)
            array.append(value)
        return array

    