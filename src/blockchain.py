import hashlib
import json
import os
import time
from datetime import datetime


class Block:
    """Represents a single block in the blockchain."""

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        # proof‑of‑work nonce
        self.nonce = 0
        self.hash = self.calculate_hash()

    def mine_block(self, difficulty):
        """Perform proof‑of‑work by finding a hash with required leading zeros."""
        assert difficulty >= 0, "Difficulty must be non‑negative"
        prefix = '0' * difficulty
        start = time.time()
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()
        end = time.time()
        elapsed = end - start
        print(f"Block {self.index} mined: {self.hash} (nonce={self.nonce})")
        print(f"Time taken: {elapsed:.2f} seconds, difficulty={difficulty}")

    def calculate_hash(self):
        """
        Calculate SHA‑256 hash of the block.
        Serializes all block attributes (including nonce) to ensure consistency.
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return (f"Block(index={self.index}, hash={self.hash[:8]}..., "
                f"prev={self.previous_hash[:8]}..., nonce={self.nonce})")

    # --- serialization helpers ------------------------------------------------
    def to_dict(self):
        """Convert block to primitive dict for JSON storage."""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }

    @staticmethod
    def from_dict(d):
        """Reconstruct a Block instance from a dict previously produced by to_dict()."""
        blk = Block(d['index'], d['timestamp'], d['data'], d['previous_hash'])
        blk.nonce = d['nonce']
        blk.hash = d['hash']
        return blk


class Blockchain:
    """Chain manager with PoW, mempool and file persistence."""

    # number of leading zeros required in hash
    difficulty = 5

    def __init__(self):
        self.chain = []
        self.pending_transactions = []  # mempool

        # file in project root used for persistence
        self.chain_file_path = os.path.join(
            os.path.dirname(__file__),
            'chain_data.json'
        )

        # attempt load; if it fails, start fresh
        if not self._load_chain_from_file():
            self.create_genesis_block()
            self._save_chain_to_file()

    # --- persistence helpers ---------------------------------------------------
    def _save_chain_to_file(self):
        """Serialize `self.chain` and write to JSON file."""
        try:
            data = [blk.to_dict() for blk in self.chain]
            with open(self.chain_file_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Chain saved to {self.chain_file_path}")
        except Exception as e:
            print(f"✗ error saving chain: {e}")

    def _load_chain_from_file(self):
        """Load chain from disk; return True if loaded, False if no file or error."""
        try:
            if os.path.exists(self.chain_file_path):
                with open(self.chain_file_path, 'r') as f:
                    data = json.load(f)
                self.chain = [Block.from_dict(d) for d in data]
                print(f"✓ Chain loaded from {self.chain_file_path} "
                      f"({len(self.chain)} blocks)")
                return True
        except Exception as e:
            print(f"✗ error loading chain: {e}")
        return False

    # --- existing functionality ----------------------------------------------
    def create_genesis_block(self):
        """Create the first block with previous_hash `'0'`."""
        genesis = Block(0, datetime.now().isoformat(), "Genesis Block", "0")
        self.chain.append(genesis)
        print("✓ Genesis block created")

    def create_transaction(self, sender, recipient, amount):
        """Append a new transaction to the pending pool."""
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self, miner_reward_address):
        """Mine all pending transactions plus a reward; persist the chain."""
        reward_tx = {"sender": "0", "recipient": miner_reward_address, "amount": 50}
        txs = [reward_tx] + self.pending_transactions
        last = self.chain[-1]
        new_block = Block(len(self.chain), datetime.now().isoformat(),
                          txs, last.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        self._save_chain_to_file()
        return new_block

    def is_chain_valid(self, chain=None):
        """Basic validation: hashes, links, PoW, and non‑negative amounts."""
        if chain is None:
            chain = self.chain
        for i, blk in enumerate(chain):
            if blk.hash != blk.calculate_hash():
                return False
            if not blk.hash.startswith('0' * self.difficulty):
                return False
            if i > 0 and blk.previous_hash != chain[i-1].hash:
                return False
            if isinstance(blk.data, list):
                for tx in blk.data:
                    if tx["amount"] <= 0:
                        return False
        return True

    def replace_chain(self, new_chain):
        """Adopt a longer, valid chain and persist it."""
        if len(new_chain) > len(self.chain) and self.is_chain_valid(new_chain):
            self.chain = new_chain
            print(f"Chain replaced with longer valid chain (len={len(new_chain)})")
            self._save_chain_to_file()
            return True
        return False

    def print_chain(self):
        """Pretty‑print every block."""
        for blk in self.chain:
            print(f"Index: {blk.index}")
            print(f"Hash: {blk.hash}")
            print(f"Previous Hash: {blk.previous_hash}")
            print(f"Nonce: {blk.nonce}")
            if isinstance(blk.data, list):
                print("Transactions:")
                for tx in blk.data:
                    print(f"  {tx['sender']} -> {tx['recipient']}: {tx['amount']}")
            else:
                print(f"Data: {blk.data}")
            print()

# ... rest of the __main__ simulation code remains unchanged ...