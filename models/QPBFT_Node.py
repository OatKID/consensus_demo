from models.Node import Node
from models.Role import Role
import random
import numpy
class QPBFT_Node(Node):
    def __init__(self, idUser: int,faulty: bool = False, role:Role=Role.VOTER, malicious: bool = False) -> None:
        super().__init__(idUser, faulty)
        self.role = role
        self.reliable_score = 0
    
    def __repr__(self) -> str:
        return f"IdUser => {self.idUser}, Score => {self.reliable_score:.2f}, Role => {self.role.value:>8}, Faulty => {str(self.faulty):>6}, Send_Message => {str(self.send_message_log[:-1] if self.send_message_log else "\'\'"):<35}, Messages_Log => {self.messages_log}"
    
    def generate_score(self) -> list[int]:
        # * [a11, a12, a13, a21, a22, a23] ~ [a1, a2, a3, a4, a5, a6]
        array = numpy.random.uniform(size=6)
        return array
    
    def set_reliable_score(self, score) -> None:
        self.reliable_score = score
    
    def set_reliable_score_normalize(self, score_normalize) -> None:
        self.reliable_score_normalize = score_normalize

    