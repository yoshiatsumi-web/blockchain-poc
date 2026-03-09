
# Blockchain Implementation Step 1: Core Data Structure

## Overview
This specification describes a minimum viable blockchain implementation focusing on block structure and hash linkage.

## Block Class

```python
import hashlib
import json
from datetime import datetime

class Block:
    """Represents a single block in the blockchain."""
    
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate SHA-256 hash of the block.
        Serializes all block attributes to ensure consistency.
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def __repr__(self):
        return (f"Block(index={self.index}, hash={self.hash[:8]}..., "
                f"previous_hash={self.previous_hash[:8]}...)")
```

## Blockchain Management

```python
class Blockchain:
    """Manages the chain of blocks."""
    
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block with previous_hash of '0'."""
        genesis = Block(0, datetime.now().isoformat(), "Genesis Block", "0")
        self.chain.append(genesis)
    
    def add_block(self, data):
        """Create and add a new block, using the last block's hash as previous_hash."""
        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
        return new_block
    
    def print_chain(self):
        """Display all blocks in the chain."""
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Data: {block.data}\n")
```

## Hash Linkage Mechanism

Each block contains the hash of its predecessor. This creates an immutable chain—modifying any block invalidates all subsequent hashes, ensuring data integrity.

## Usage Example

```python
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block({"tx": "Alice -> Bob: 10"})
    blockchain.add_block({"tx": "Bob -> Charlie: 5"})
    blockchain.print_chain()
```
