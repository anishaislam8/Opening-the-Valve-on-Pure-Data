import sys
import os
import json
import networkx as nx
from pathlib import Path

folder= sys.argv[1]
print(folder)
folder_name = "/data/play/aislam4/thesis/pd_parsed/stats_revisions/" + folder



for filename in os.listdir(folder_name):
    
    with open(os.path.join(folder_name, filename), 'r') as f: # open in readonly mode
        # read the json file
        new_path_file_name = Path(filename).stem
        if os.stat(os.path.join(folder_name, filename)).st_size != 0:
            
            data = json.load(f)

            try:
                connections = data["connections"]
                all_objects = data["all_objects"]
            except:
                connections = []
                all_objects = []
            
            if len(connections) > 0:

                object_dict = {}
                for obj in all_objects:
                    if obj["box"]["object_type"] in ["list"]:
                        object_dict[obj["box"]["id"]] = obj["box"]["text"]
                    else:
                        object_dict[obj["box"]["id"]] = obj["box"]["object_type"]

                
                sources = [connection["patchline"]["source"][0] for connection in connections]
                destinations = [connection["patchline"]["destination"][0] for connection in connections]

                nodes = set(sources + destinations)
                
                G = nx.DiGraph()
                G.add_nodes_from(nodes)
                G.add_edges_from([(connection["patchline"]["source"][0], connection["patchline"]["destination"][0]) for connection in connections])
                
                
                roots = [v for v, d in G.in_degree() if d == 0]
                leaves = [v for v, d in G.out_degree() if d == 0]

                longest_path = []
                longest_path_length = -1
                
                for root in roots :
                    for leaf in leaves :
                        for path in nx.all_simple_paths(G, root, leaf) :
                            if len(path) > longest_path_length:
                                longest_path_length = len(path)
                                longest_path = path
               
                longest_path = [object_dict[node] for node in longest_path]
                
                if longest_path_length == -1:
                    with open("/data/play/aislam4/thesis/pd_parsed/paths_revisions/no_root_1.txt", "a") as outfile:
                        outfile.write(folder + "/" + filename + "\n")
                
                else:
                    
                
                    with open("/data/play/aislam4/thesis/pd_parsed/paths_revisions/paths/"+folder+"/" + new_path_file_name + ".txt", "w") as outfile:
                        outfile.write(str(longest_path))
                    with open("/data/play/aislam4/thesis/pd_parsed/paths_revisions/path_lengths_1.txt", "a") as outfile:
                        outfile.write(folder + "," + new_path_file_name + "," + str(longest_path_length) + "\n")

            else:

                with open("/data/play/aislam4/thesis/pd_parsed/paths_revisions/paths/"+folder+"/" + new_path_file_name + ".txt", "w") as outfile:
                        outfile.write("[]")
                with open("/data/play/aislam4/thesis/pd_parsed/paths_revisions/path_lengths_1.txt", "a") as outfile:
                    outfile.write(folder + "," + new_path_file_name + "," + str(0) + "\n")

               