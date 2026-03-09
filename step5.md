# Persisting the Chain to Disk

Objective: make the Blockchain class save its chain to a local JSON file and reload it on startup.

1. Choose a file – e.g. chain_data.json in the project root.

2. Block serialization

- add to_dict()/from_dict() helpers to Block class so blocks can be encoded/decoded as JSON.

3. File‑IO helpers

- \_save_chain_to_file() – dump self.chain (via to_dict) to the JSON file.
- \_load_chain_from_file() – if file exists, read it, rebuild blocks with from_dict, assign to self.chain and return True; otherwise return False.

4. Constructor changes

- set self.chain_file_path to the chosen path (use os.path.dirname(**file**) to locate project).
- in **init**() call \_load_chain_from_file(); if it returns False, call create_genesis_block() and immediately save the fresh chain.

5. Trigger saves

- make mining (mine_pending_transactions) and replace_chain persist the updated chain on success.

# Result:

Each Blockchain instance boots from the saved chain if present, otherwise starts with a genesis block, and all modifications are written back to disk.
