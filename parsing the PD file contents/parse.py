from parsers.pd.pdparser import main as pdparser
import json
import sys

file_name = sys.argv[1]

stats = pdparser(file_name)
json_output = json.dumps(stats, indent=4)

with open("example PD file and parsed output/example.json", "w") as f:
    f.write(json_output)