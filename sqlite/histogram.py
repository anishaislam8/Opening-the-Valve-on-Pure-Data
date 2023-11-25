import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("csvs/authors_projects_unique_filtered_hashed.csv")

grouped = df.groupby('Project_Name')

# Find the number of rows in each group
row_count = grouped.size()

# Display the result
data = row_count.values

plt.hist(data, color='lightgreen', ec='black', bins=15)
plt.yscale('log')
plt.xlabel('Number of Authors-Committers Per Project')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Authors-Committers Per Project')
plt.show()


author_count = grouped['Author_Name'].nunique()
data = author_count.values
plt.hist(data, color='lightgreen', ec='black', bins=15)
# plt.yscale('symlog', linthresh=0.05)
plt.yscale('log')
plt.xlabel('Number of Authors Per Project')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Authors Per Project')
plt.show()


df = pd.read_csv("csvs/nodes_edges_per_file.csv")
nodes = df['Nodes'].values
edges = df['Edges'].values


plt.hist(nodes, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Nodes Per File')
plt.ylabel('Number of Files (Log Scale)')
plt.title('Histogram of Number of Nodes Per File')
plt.show()


plt.hist(edges, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Connections Per File')
plt.ylabel('Number of Files (Log Scale)')
plt.title('Histogram of Number of Connections Per File')
plt.show()

df = pd.read_csv("csvs/nodes_edges_per_project.csv")
nodes = df['Nodes'].values
edges = df['Edges'].values


plt.hist(nodes, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Nodes Per Project')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Nodes Per Project')
plt.show()


plt.hist(edges, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Connections Per Project')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Connections Per Project')
plt.show()

# describe the data
# print(df["Nodes"].describe())
# print(df["Edges"].describe())


df = pd.read_csv("csvs/number_of_files_per_project.csv")
revision_files = df['Total_Revisions'].values
source_files = df['Source_Files'].values



plt.hist(revision_files, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Revisions Per Project')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Revisions Per Project')
plt.show()


plt.hist(source_files, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Number of Pd Files Per Project (Without Revisions)')
plt.ylabel('Number of Projects (Log Scale)')
plt.title('Histogram of Number of Pd Files Per Project (Without Revisions)')
# plt.show()


df = pd.read_csv("csvs/differences.csv")
nodes = df['Diff_Nodes'].values
edges = df['Diff_Edges'].values


plt.hist(nodes, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Difference of Nodes Per Revision File')
plt.ylabel('Number of Files (Log Scale)')
plt.title('Histogram of Difference of Nodes Per Revision File')
plt.show()


plt.hist(edges, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Difference of Connections Per Revision File')
plt.ylabel('Number of Files (Log Scale)')
plt.title('Histogram of Difference of Connections Per Revision File')
plt.show()