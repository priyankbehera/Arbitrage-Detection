import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


adjacency_matrix = np.array([[0, 2, 3, 0],  # Node A to B (2), A to C (3)
                              [0, 0, 4, 0],  # Node B to C (4)
                              [0, 0, 0, 5],  # Node C to D (5)
                              [0, 0, 0, 0]]) # Node D has no outgoing edges

# Create a directed graph from the adjacency matrix
G = nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph)

# Add weights to the edges
for i, j in G.edges():
    G[i][j]['weight'] = adjacency_matrix[i, j]

# Optionally, set node labels (default is 0, 1, 2,...)
G = nx.relabel_nodes(G, {0: 'A', 1: 'B', 2: 'C', 3: 'D'})

# Print the edges with weights
print("Edges of the directed graph with weights:", [(u, v, d['weight']) for u, v, d in G.edges(data=True)])

# Draw the graph
pos = nx.spring_layout(G)  # Positioning of nodes
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
