from Block import Block

class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self._length = 0
    
    # Making new block to append in blockchain
    def add_block(self, transaction:str) -> Block:
        id_block = len(self.chain) + 1
        block = Block(id_block, "0", transaction)
        self.chain.append(block)
        self._length += 1
        return block
    
    def get_chain(self) -> list:
        return self.chain
    
    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i-1]
            current_block = self.chain[i]
            if previous_block.hash != current_block.previous_hash:
                return False

            if current_block.hash != current_block.calculate_hash():
                return False
        
        return True

if __name__ == "__main__":
    blockchain1 = Blockchain()

    blockchain1.add_block("Hello world")
    blockchain1.add_block("Make Consensus algorithm")
    blockchain1.add_block("Siwakorn Paswang")

    for i in blockchain1.get_chain():
        print(i)
