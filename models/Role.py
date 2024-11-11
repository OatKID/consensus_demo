from enum import Enum

class Role(Enum):
    MANAGER = "Manager"
    VOTER = "Voter"
    MASTER = "Master"
    SLAVE = "Slave"
