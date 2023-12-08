#!/bin/bash

python3 create_content_table.py
python3 add_new_tables.py
./extract_renames_db.sh
python3 update_revisions_and_add_indices.py
