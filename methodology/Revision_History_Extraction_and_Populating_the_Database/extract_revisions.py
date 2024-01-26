import os
# fix the path to the pdparser accordingly
from parsers.pd.pdparser import main as pdparser
import sys
import json
from pydriller.git import Git
import tempfile
from datetime import datetime
import subprocess
from pathlib import Path
import pysqlite3
import hashlib

# fix the database location
connection = pysqlite3.connect("../../database.db")
cursor = connection.cursor()
cursor.execute('BEGIN TRANSACTION')

def calculate_sha256(data):
    # Convert data to bytes if it’s not already
    if isinstance(data, str):
        data = data.encode()

    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()

    return sha256_hash 
def is_sha1(maybe_sha):
    if len(maybe_sha) != 40:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True

def get_revisions_and_run_parser(cwd, project_name, main_branch, debug=False):
    proc1 = subprocess.run(['git --no-pager log --pretty=tformat:"%H" "origin/{}" --no-merges'.format(main_branch)], stdout=subprocess.PIPE, cwd=cwd, shell=True)
    proc2 = subprocess.run(['xargs -I{} git ls-tree -r --name-only {}'], input=proc1.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
    proc3 = subprocess.run(['grep -i "\.pd$"'], input=proc2.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
    proc4 = subprocess.run(['sort -u'], input=proc3.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
    filenames = proc4.stdout.decode().strip().split('\n')

    # for all pd files in ths project
    for f in filenames:
        proc1 = subprocess.run(['git --no-pager log -z --numstat --follow --pretty=tformat:"{}¬%H" -- "{}"'.format(f,f)], stdout=subprocess.PIPE, cwd=cwd, shell=True)
        proc2 = subprocess.run(["cut -f3"], input=proc1.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
        proc3 = subprocess.run(["sed 's/\d0/¬/g'"], input=proc2.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
        proc4 = subprocess.run(['xargs -0 echo'], input=proc3.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
        filename_shas = proc4.stdout.decode().strip().split('\n')
        filename_shas = [x for x in filename_shas if x != '']

        #if 2 ¬ then it is the original filename that we are trying to trace back (includes original filename, commit)
        #if 3 ¬ then it is not renamed (includes renamed filename, original filename, commit)
        #if starts with ¬ then it is renamed (includes pre-filename, renamed filename, original filename, commit)
        #if 1 ¬ then it is a beginning file with no diff; skip
        
        proc1 = subprocess.run(['git --no-pager log --all --pretty=tformat:"%H" -- "{}"'.format(f)], stdout=subprocess.PIPE, cwd=cwd, shell=True) # Does not produce renames
        all_shas = proc1.stdout.decode().strip().split('\n') 
        all_shas = [x for x in all_shas if x != '']
        all_sha_names = {}
        
        for x in all_shas:
            all_sha_names[x] = None

        # get filenames for each commit
        for fn in filename_shas: # start reversed, oldest to newest
            separator_count = fn.strip().count('¬')
            split_line = fn.strip('¬').split('¬')
            #print(split_line)
            file_contents = ''
            
            if separator_count == 2:
                c = split_line[-1]

                if not is_sha1(c):
                    # Edge case where line doesn't have a sha
                    #print(split_line)
                    continue

                all_sha_names[c] = split_line[0]
                #print("Separator count 2: assigning {} to {}".format(c, split_line[0]))
        
            elif fn[0] == '¬':
                new_name = split_line[0]
                c = split_line[-1]

                if not is_sha1(c):
                    # Edge case where line doesn't have a sha
                    #print(split_line)
                    continue

                all_sha_names[c] = new_name
                #print("starting with separator: assigning {} to {}".format(c, split_line[-4]))
                
            elif separator_count == 3:
                # print(split_line[-1])
                new_name = split_line[0]
                c = split_line[-1]

                if not is_sha1(c):
                    # Edge case where line doesn't have a sha
                    #print(split_line)
                    continue

                all_sha_names[c] = new_name
                #print("Separator count 3: assigning {} to {}".format(c, split_line[-3]))
                
            elif separator_count == 1:
                continue
        
            else:
                raise ValueError('Unknown case for file')
 


        all_sha_dates = {}
        for c in all_sha_names.keys():
            commit_date = subprocess.run(['git log -1 --format=%ci {}'.format(c)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=cwd, shell=True).stdout.decode()
            parsed_date = datetime.strptime(commit_date.strip(), '%Y-%m-%d %H:%M:%S %z')
            

            all_sha_dates[c] = parsed_date

        # fill in the gaps
        prev_fn = f
        for c in all_sha_names.keys():
            if all_sha_names[c] is None:
                all_sha_names[c] = prev_fn
            prev_fn = all_sha_names[c]
        
        stats = {}

        
            
        for c in sorted(all_sha_dates, key=all_sha_dates.get): # start oldest to newest
           
            new_name = all_sha_names[c]
            

            commit_date = subprocess.run(['git log -1 --format=%ci {}'.format(c)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=cwd, shell=True).stdout.decode()
            parsed_date = datetime.strptime(commit_date.strip(), '%Y-%m-%d %H:%M:%S %z')
            parsed_date_str = parsed_date.strftime('%Y-%m-%d %H:%M:%S %z')


            # with open("/pd_parsed/csvs/project_file_revision_commitsha_commitdate_1.txt", "a") as outfile:
            #     outfile.write("{}_COMMA_{}_COMMA_{}_COMMA_{}_COMMA_{}\n".format(project_name, f, new_name, c, parsed_date_str))


            file_contents = ''
            
            try:
                contents1 = subprocess.run(['git show {}:"{}"'.format(c, new_name)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=cwd, shell=True)
                contents2 = subprocess.run(["sed 's/\\;/_SLASH_SEMICOLON_/g'"], input=contents1.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
                contents3 = subprocess.run(["sed 's/;#X/;\\n#X/g'"], input=contents2.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
                contents4 = subprocess.run(["sed 's/;#N/;\\n#N/g'"], input=contents3.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
                contents5 = subprocess.run(["sed 's/; #X/;\\n#X/g'"], input=contents4.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
                contents6 = subprocess.run(["sed 's/; #N/;\\n#N/g'"], input=contents5.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
                contents7 = subprocess.run(["sed 's/_SLASH_SEMICOLON_/\\;/g'"], input=contents6.stdout, stdout=subprocess.PIPE, cwd=cwd, shell=True)
                
                file_contents = contents7.stdout.decode("utf-8", "ignore")
            except:
                file_contents = ''
            
            
            # Parse the code into intermediate representation
            with tempfile.NamedTemporaryFile(delete=False) as fp:
                fp.write(file_contents.encode())
            
            
            try:
                stats = pdparser(fp.name)
                
            except:
                stats = {"edges":0,"nodes":0, "node_types":{}, "all_objects":[], "connections": []}
            os.remove(fp.name) 
            #stats["commit_date"] = parsed_date_str
            #stats["commit_sha"] = c

            try:
                node = stats["nodes"]
                edge = stats["edges"]
            except:
                node = 0
                edge = 0

            json_output = json.dumps(stats, indent=4)
            hash_value = calculate_sha256(str(json_output))
            
            new_original_file_name = f.replace(",", "_COMMA_")
            new_name = new_name.replace(",", "_COMMA_")
            
            cursor.execute("INSERT INTO Revisions (Project_Name, File, Revision, Commit_SHA, Commit_Date, Hash, Nodes, Edges) VALUES(?,?,?,?,?,?,?,?)", (project_name, new_original_file_name, new_name, c, parsed_date_str, hash_value, node, edge))
            cursor.execute("INSERT INTO Contents (Hash, Content) VALUES(?,?) ON CONFLICT(Hash) DO NOTHING", (hash_value, str(json_output)))
        
    # end one pd file

        

def main(filename: str):
    project_name, main_branch = filename.split(',')
    print(project_name)
    git_object = Git(f'pd_mirrored_extracted/{project_name}')
    git_object.checkout(main_branch)
    try:
        get_revisions_and_run_parser(f'pd_mirrored_extracted/{project_name}', project_name, main_branch)
    except Exception as e:
        print(e)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)


