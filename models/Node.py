class Node:
    def __init__(self, idUser:int, priority:int) -> None:
        self.idUser = idUser
        self.is_leader = False
        self.priority = priority
        self.key = ""
        self.messages_log = []

    def setLeader(self):
        self.is_leader = True
    
    def unsetLeader(self):
        self.is_leader = False
    
    def setKey(self, key:str):
        self.key = key