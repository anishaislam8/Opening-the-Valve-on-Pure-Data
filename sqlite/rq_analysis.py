import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("csvs/differences_final.csv")
df["Diff_Nodes"] = df["Diff_Nodes"].astype(int)
df["Diff_Edges"] = df["Diff_Edges"].astype(int)
nodes = df['Diff_Nodes'].values
edges = df['Diff_Edges'].values

print(df["Diff_Nodes"].describe())
print(df["Diff_Edges"].describe())

print("Nodes <= 27: ", len(nodes[nodes <= 27]))
print("Edges <= 17: ", len(edges[edges <= 17]))


plt.hist(nodes, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Difference in Nodes Per Revision of a PD File')
plt.ylabel('Number of Total Revisions (Log Scale)')
plt.title('Histogram of Difference in Nodes Per Revision of a PD File')
plt.show()


plt.hist(edges, color='lightgreen', ec='black', bins=20)
plt.yscale('log')
plt.ticklabel_format(axis='x', style='plain')
plt.xlabel('Difference in Connections Per Revision of a PD File')
plt.ylabel('Number of Total Revisions (Log Scale)')
plt.title('Histogram of Difference in Connections Per Revision of a PD File')
plt.show()

# median value
print(df["Diff_Nodes"].sort_values().median())
print(df["Diff_Edges"].sort_values().median())