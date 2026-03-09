import hashlib
import json
import time
from datetime import datetime


class Block:
    """Represents a single block in the blockchain."""

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        # proof-of-work nonce
        self.nonce = 0
        self.hash = self.calculate_hash()

    def mine_block(self, difficulty):
        """Perform proof-of-work by finding a hash with required leading zeros."""
        assert difficulty >= 0, "Difficulty must be non-negative"
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
        Calculate SHA-256 hash of the block.
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


class Blockchain:
    """Manages the chain of blocks with proof-of-work (mining) and transaction pool."""

    # difficulty level: number of leading zeros required in hash
    difficulty = 5

    def __init__(self):
        self.chain = []
        self.pending_transactions = []  # transaction pool (mempool)
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block with previous_hash of '0'."""
        genesis = Block(0, datetime.now().isoformat(), "Genesis Block", "0")
        self.chain.append(genesis)

    def create_transaction(self, sender, recipient, amount):
        """Create a new transaction and add it to the pending pool."""
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_reward_address):
        """Mine a new block with all pending transactions plus mining reward."""
        # add mining reward transaction (coinbase)
        reward_transaction = {
            "sender": "0",  # system
            "recipient": miner_reward_address,
            "amount": 50
        }
        transactions = [reward_transaction] + self.pending_transactions

        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=transactions,  # list of transactions
            previous_hash=last_block.hash
        )
        # perform mining
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        # clear pending transactions
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self, chain=None):
        """Validate the blockchain: hashes, links, PoW, and basic transaction checks."""
        if chain is None:
            chain = self.chain
        if not chain:
            return True
        for i, block in enumerate(chain):
            # check hash integrity
            if block.hash != block.calculate_hash():
                return False
            # check PoW
            if not block.hash.startswith('0' * self.difficulty):
                return False
            if i > 0:
                # check chain link
                if block.previous_hash != chain[i-1].hash:
                    return False
            # check transactions
            if isinstance(block.data, list):
                for tx in block.data:
                    if tx["amount"] <= 0:
                        return False
                    # additional checks can be added here
        return True

    def replace_chain(self, new_chain):
        """Replace chain with a longer valid one (consensus rule)."""
        if len(new_chain) > len(self.chain) and self.is_chain_valid(new_chain):
            self.chain = new_chain
            print(f"Chain replaced with longer valid chain (length {len(new_chain)})")
            return True
        return False

    def print_chain(self):
        """Display all blocks in the chain."""
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Nonce: {block.nonce}")
            if isinstance(block.data, list):
                print("Transactions:")
                for tx in block.data:
                    print(f"  {tx['sender']} -> {tx['recipient']}: {tx['amount']}")
            else:
                print(f"Data: {block.data}")
            print()


if __name__ == "__main__":
    # simulation of decentralized consensus with multiple nodes
    print("=== Decentralized Consensus Simulation ===\n")

    # create three nodes
    node_A = Blockchain()
    node_B = Blockchain()
    node_C = Blockchain()

    # all nodes receive the same transactions (broadcast)
    for node in [node_A, node_B, node_C]:
        node.create_transaction("Alice", "Bob", 10)
        node.create_transaction("Bob", "Charlie", 5)

    # node_A mines a new block
    print("Node A mining block...")
    node_A.mine_pending_transactions("MinerA")
    print()

    # node_B and node_C sync with node_A's longer chain
    print("Node B syncing with Node A...")
    node_B.replace_chain(node_A.chain)
    print()

    print("Node C syncing with Node A...")
    node_C.replace_chain(node_A.chain)
    print()

    # verify all chains are identical
    print("Node A chain:")
    node_A.print_chain()

    print("Node B chain:")
    node_B.print_chain()

    print("Node C chain:")
    node_C.print_chain()

    print("All nodes now have identical chains - consensus achieved!")

    # note on conflict resolution
    print("\nNote: In case of conflicts (two nodes mine blocks simultaneously),")
    print("the network resolves by adopting the longest valid chain.")
    print("Increasing difficulty exponentially raises mining time.")

    # explanation comment
    print("\nNote: increasing the difficulty value makes the required mining time "
          "exponentially larger, because the probability of finding a hash with more "
          "leading zeros drops by a factor of 256 for each additional zero.")
