#!/bin/bash

query="$1"
sqlite3 database.db "$query"