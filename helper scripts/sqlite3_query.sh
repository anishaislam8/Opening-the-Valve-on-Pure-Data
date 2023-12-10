#!/bin/bash

query="$1"
sqlite3 revision_hashes.db "$query"