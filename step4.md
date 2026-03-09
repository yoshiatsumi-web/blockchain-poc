# Blockchain Implementation Step 4 (P2P & Decentralized Consensus)

# Request

Please update the previous Python blockchain code to implement Step 4: Decentralized Consensus Simulation. This step simulates how multiple nodes in a network keep their chains in sync and resolve conflicts using the "Longest Chain Rule."

# Implementation Requirements

Multiple Nodes: Create a way to simulate multiple Blockchain instances (e.g., node_A, node_B, node_C).

## Network Synchronization:

1. Implement a method replace_chain(new_chain) that validates a received chain.

2. The Consensus Rule: If a node receives a valid chain that is longer than its current one, it should replace its own chain with the longer one.

## Conflict Simulation:

1. Show a scenario where node_A mines a new block, and node_B and node_C must update their chains to match node_A.

2. Show a "conflict" scenario: node_B mines a different block at the same time. Demonstrate how the network eventually chooses the "longest" (most computationally difficult) chain once the next block is added.

## Chain Validation:

1. Create a method is_chain_valid() that iterates through the entire chain to ensure:
   1. All hashes are correctly linked.
   2. Every block satisfies the Proof of Work (difficulty).
   3. All transactions are consistent.

# Output Format

A single, runnable Python file.

## A demonstration in the console showing:

- Node A mining a block.
- Node B and C "syncing" their chains with Node A.
- A printout of the chains of all three nodes to prove they are identical.
