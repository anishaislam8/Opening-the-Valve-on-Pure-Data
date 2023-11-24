#!/bin/bash

python3 create_new_database.py
python3 update_revisions_and_add_indices.py
python3 create_hash_table.py
./create_hash_content.sh
