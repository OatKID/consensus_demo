import datetime
import hashlib
class Block:
    def __init__(self, id_block:int, previous_hash:str, transaction:str, timestamp:str = str(datetime.datetime.now())) -> None:
        self.id_block = id_block
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transaction = transaction
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_string = f"{self.id_block} {self.previous_hash} {self.timestamp} {self.transaction}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"Id_block: {self.id_block} Previous_hash: {self.previous_hash} Timestamp: {self.timestamp} Transaction: {self.transaction} Hash: {self.hash}"

if __name__ == "__main__":
    block1 = Block(0, "0", "Hello world")
    block2 = Block(1, "2", "Goodbye world")
    print(block1)
    print(block2)