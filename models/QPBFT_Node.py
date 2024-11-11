from models.Node import Node
from models.Role import Role
import random
class QPBFT_Node(Node):
    def __init__(self, idUser: int,faulty: bool = False, role:Role=Role.VOTER) -> None:
        super().__init__(idUser, faulty)
        self.role = role
        self.security_values = self._generate_score(3)
        self.availability_value = self._generate_score(3)
    
    def __repr__(self) -> str:
        return f"IdUser => {self.idUser}, Role => {"M" if self.role.value=="Management" else "V"}, Send_messages_log => {self.send_messages_log}, Receive_messages_log => {self.receive_messages_log}"
    
    def _generate_score(self, num_value):
        array = []
        for i in range(num_value):
            value = random.randint(0, 100)
            array.append()
        return array

    