# Copilot Prompt:

Blockchain Implementation Step 3 (Transaction Pool)

# Request

Please update the previous Python blockchain code to implement Step 3: Transaction Pool (MemPool). This step introduces a mechanism to handle multiple transactions and package them into a single block after mining.

# Implementation Requirements

Transaction Pool: Add a list called pending_transactions to the main blockchain management logic (or a Blockchain class).

## Create Transaction Method:

Implement a function create_transaction(sender, recipient, amount) that:

Formats the transaction as a dictionary.

Appends it to the pending_transactions list.

## Mining Reward:

Add a specialized transaction to every new block (often called a "Coinbase Transaction") that rewards the miner with a fixed amount of coins (e.g., 50 coins).

## Updated Mining Process:

Create a method mine_pending_transactions(miner_reward_address).

This method should take all transactions from pending_transactions, add the reward transaction, and package them into a new Block.

Once the block is successfully mined and added to the chain, clear the pending_transactions list so they aren't mined again.

## Balance Checker:

Implement a simple function get_balance(address) that:

Iterates through the entire blockchain.

Calculates the total balance for a specific address by tracking all "sender" and "recipient" entries.

# Output Format

A single, runnable Python file.

A demonstration in the code that:

Adds 3-4 transactions.

Mines them into Block #1.

Adds 2 more transactions.

Mines them into Block #2.

Prints the final balances of the participants.
