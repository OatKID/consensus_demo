class Node:
    def __init__(self, idUser:int, timestamp:str) -> None:
        self.idUser = idUser
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"IdUser=> {self.idUser}"