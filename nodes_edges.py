import json
import os
import sys
import subprocess

folder= sys.argv[1]
folder_name = "/data/play/aislam4/thesis/pd_parsed/stats_revisions/" + folder
nodes_in_this_project = 0
edges_in_this_project = 0

for filename in os.listdir(folder_name):
    with open(os.path.join(folder_name, filename), 'r') as f: # open in readonly mode
        # read the json file
        if os.stat(os.path.join(folder_name, filename)).st_size != 0:
            
            original_part = filename.split("_CMMT_")[0]
            new_original_file_name = original_part.replace(",", "_COMMA_")    
            new_original_file_name = new_original_file_name.replace("_FFF_", "/")   
            # suggestion: use the original file name extension and check if the filename is actually empty, in that case, no need to add extensions.  
            new_original_file_name_pd = new_original_file_name + ".pd" 
            commit = filename.split("_CMMT_")[1].split(".json")[0]
            
            data = json.load(f)
            try:
                nodes_in_this_file = int(data['nodes'])
                edges_in_this_file = int(data['edges'])
            except:
                nodes_in_this_file = 0
                edges_in_this_file = 0


            with open("/data/play/aislam4/thesis/pd_parsed/csvs/nodes_edges_per_file.csv", 'a') as f:
                f.write(folder + "," + new_original_file_name_pd + "," + commit + "," + str(nodes_in_this_file) + "," + str(edges_in_this_file))
                f.write("\n")
            
            nodes_in_this_project += nodes_in_this_file
            edges_in_this_project += edges_in_this_file
    


with open("/data/play/aislam4/thesis/pd_parsed/csvs/nodes_edges_per_project.csv", 'a') as f:
    f.write(folder + "," + str(nodes_in_this_project) + "," + str(edges_in_this_project))
    f.write("\n")
            



