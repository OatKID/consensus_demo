from models.Node import Node
import random
class PBFT_Simulator:
    def __init__(self, num_node:int) -> None:
        self.nodes = [(Node(i, random.randint(0, 10)), []) for i in range(num_node)]


simulator = PBFT_Simulator(10)
print(simulator.nodes)
