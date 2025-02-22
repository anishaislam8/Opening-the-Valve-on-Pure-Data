import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

connection = sqlite3.connect("../database.db")
cursor = connection.cursor()

'''

Distribution of nodes and edges

'''

cursor.execute('''SELECT Nodes, Edges FROM Revisions;''')
nodes_edges = cursor.fetchall()

# Create a DataFrame

df = pd.DataFrame(nodes_edges, columns=['Nodes', 'Edges'])
nodes = df['Nodes'].values
edges = df['Edges'].values
print(df["Nodes"].describe())
print(df["Edges"].describe())


cursor.execute('''SELECT COUNT(nodes) FROM revisions WHERE nodes >= 1 and nodes <= 64;''')
num_nodes_1_64 = cursor.fetchall()
print("Number of nodes between 1 and 64: ", num_nodes_1_64)

cursor.execute('''SELECT COUNT(edges) FROM revisions WHERE edges >= 1 and edges <= 51;''')
num_edges_1_51 = cursor.fetchall()
print("Number of edges between 1 and 51: ", num_edges_1_51)

cursor.execute('''SELECT COUNT(nodes) FROM revisions WHERE nodes = 0;''')
num_nodes_0 = cursor.fetchall()
print("Number of nodes = 0: ", num_nodes_0)

cursor.execute('''SELECT COUNT(edges) FROM revisions WHERE edges = 0;''')
num_edges_0 = cursor.fetchall()
print("Number of edges = 0: ", num_edges_0)

cursor.execute('''SELECT COUNT(edges) FROM revisions WHERE edges >= 30000;''')
num_edges_gt_30000 = cursor.fetchall()
print("Number of edges >= 30000: ", num_edges_gt_30000)

cursor.execute('''SELECT project_name, file, COUNT(nodes) FROM revisions WHERE nodes >= 30000;''')
num_nodes_gt_30000 = cursor.fetchall()
print("Number of Nodes >= 30000: ", num_nodes_gt_30000)


plt.hist(nodes, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Nodes Per Revision of a PD File')
plt.ylabel('Number of Total Revisions of PD Files (Log Scale)')
plt.title('Histogram of Number of Nodes Per Revision of a PD File')
plt.savefig('Nodes_per_file.pdf')
plt.close()

plt.hist(edges, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Connections Per Revision of a PD File')
plt.ylabel('Number of Total Revisions of PD Files (Log Scale)')
plt.title('Histogram of Number of Connections Per Revision of a PD File')
plt.savefig('Connections_per_file.pdf')
plt.close()


'''

Distribution of Revisions Per PD file

'''


cursor.execute('''SELECT Project_Name, File, COUNT(Revision) AS Revision_Count FROM Revisions WHERE File IS NOT NULL AND FILE <> '' GROUP BY Project_Name, File;''')
revisions = cursor.fetchall()

df = pd.DataFrame(revisions, columns=['Project_Name', 'File', 'Revisions'])
data = df["Revisions"].values
print(df["Revisions"].describe())

plt.hist(data, color='lightgreen', ec='black', bins=15)
plt.yscale('log')
plt.xlabel('Number of Revisions Per PD File')
plt.ylabel('Number of PD Files (Log Scale)')
plt.title('Histogram of Number of Revisions Per PD File')
plt.savefig('Revisions_per_file.pdf')
plt.close()



'''

Distribution of PD files per project

'''


cursor.execute('''SELECT Project_Name, COUNT(DISTINCT File) AS File_Count FROM Revisions GROUP BY Project_Name;''')
files = cursor.fetchall()

df = pd.DataFrame(files, columns=['Project_Name', 'Files'])
data = df["Files"].values
print(df["Files"].describe())
print(len(df[df["Files"] <= 17]))

cursor.execute('''SELECT Project_Name, COUNT(DISTINCT File) AS File_Count FROM Revisions GROUP BY Project_Name ORDER BY File_Count DESC LIMIT 3;''')
highest_files = cursor.fetchall()
print("Projects with highest files: ", highest_files)


cursor.execute('''SELECT
    p.Project_Name,
    p.Total_Commits
FROM
    Projects p
JOIN (
    SELECT
        Project_Name,
        COUNT(DISTINCT File) AS File_Count
    FROM
        Revisions
    GROUP BY
        Project_Name
    ORDER BY
        File_Count DESC
    LIMIT 3
) r ON p.Project_Name = r.Project_Name;''')
highest_files_commits = cursor.fetchall()
print("Projects with highest files and their number of commits: ", highest_files_commits)


plt.hist(data, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Pd Files Per Project (Without Revisions)')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Pd Files Per Project (Without Revisions)')
plt.savefig('PD_Files_per_project.pdf')
plt.close()



'''

Commits per project distribution

'''


cursor.execute('''SELECT Total_Commits FROM Projects;''')
total_commits = cursor.fetchall()
df = pd.DataFrame(total_commits, columns=['Commits'])
df['Commits'] = df['Commits'].astype(int)
commits = df['Commits'].values
print(df["Commits"].describe())

cursor.execute('''SELECT COUNT(total_commits) FROM projects WHERE total_commits <= 31;''')
commits_17 = cursor.fetchall()
print("Projects with <=31 commits: ", commits_17)

plt.hist(commits, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Commits Per Project')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Commits Per Project')
plt.savefig('Commits_per_project.pdf')
plt.close()



'''

Author who contributed to the PD files distribution per project

'''


cursor.execute('''SELECT Revisions.Project_Name, COUNT(DISTINCT Authors.Author_Name)
FROM Revisions
JOIN Authors ON Revisions.Commit_SHA = Authors.Commit_SHA
WHERE Revisions.file IS NOT NULL AND Revisions.file <> ''
GROUP BY Revisions.Project_Name;''')
author_count = cursor.fetchall()

df = pd.DataFrame(author_count, columns=['Project_Name', 'Authors'])
authors = df['Authors'].values
print(df["Authors"].describe())


plt.hist(authors, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.xlabel('Number of Authors Per Project For the PD Files')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Authors Per Project For the PD Files')
plt.savefig('Authors_per_project.pdf')
plt.close()

cursor.execute('''SELECT Revisions.Project_Name, COUNT(DISTINCT Authors.Author_Name) AS GroupSize
FROM Revisions
JOIN Authors ON Revisions.Commit_SHA = Authors.Commit_SHA
WHERE Revisions.file IS NOT NULL AND Revisions.file <> ''
GROUP BY Revisions.Project_Name
ORDER BY GroupSize DESC
LIMIT 5;''')
highest_author = cursor.fetchall()
print("Project with highest author count : ", highest_author)

cursor.execute('''SELECT Revisions.Project_Name, COUNT(DISTINCT Authors.Author_Name) AS AuthorCount
FROM Revisions
JOIN Authors ON Revisions.Commit_SHA = Authors.Commit_SHA
WHERE Revisions.file IS NOT NULL AND Revisions.file <> ''
GROUP BY Revisions.Project_Name
HAVING AuthorCount = 1;''')
author_1 = cursor.fetchall()
print("Projects with one authors: ", len(author_1))

cursor.close()
connection.commit()
connection.close()
