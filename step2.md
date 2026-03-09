# Request

Please update the previous Python blockchain code to implement Step 2: Proof of Work (Mining). This step introduces a computational challenge that must be solved before a block can be added to the chain.

# Implementation Requirements

Nonce Attribute: Add a nonce (Number used once) attribute to the Block class. This will be the variable that miners increment to change the block's hash.

## Difficulty Level:

Define a variable difficulty (integer). For example, if difficulty = 4, the valid hash must start with four zeros ("0000...").

## Mining Method:

Create a method named mine_block() inside the Block class:

It should repeatedly re-calculate the block's hash by incrementing the nonce.

The loop continues until the resulting hash satisfies the difficulty criteria (starts with the required number of zeros).

## Automatic Mining:

Update the block creation process so that mine_block() is called before the block is appended to the blockchain list.

## Performance Feedback:

Print the time taken to mine each block and the final hash to demonstrate that mining requires effort.

# Output Format

A single, runnable Python file.

Explanation of how increasing the difficulty exponentially increases the mining time.
