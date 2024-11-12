from models.Block import Block
import hashlib
import datetime
class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self._length = 0
    
    # Making new block to append in blockchain
    def add_block(self, transaction:str, timestamp:str) -> Block:

        # Making Genesis Block
        if self._length == 0:
            id_block = self._length + 1
            new_block = Block(id_block, hashlib.sha256(b"0").hexdigest(), transaction, timestamp)
        
        else:
            previous_block = self.chain[-1]
            id_block = self._length + 1
            new_block = Block(id_block, previous_block.hash, transaction, timestamp)

        self.chain.append(new_block)
        self._length += 1
        return new_block
    
    def get_chain(self) -> list:
        return self.chain
    
    # Verification Valid Blockchain
    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i-1]
            current_block = self.chain[i]
            if previous_block.hash != current_block.previous_hash:
                return False

            if current_block.hash != current_block.calculate_hash():
                return False
        
        return True