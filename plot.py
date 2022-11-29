import matplotlib.pyplot as plt
import networkx as nx

G = nx.read_graphml('graph.graphml')
colormap = []
for u in G.nodes:
    if u[1] == '0':
        colormap.append('blue')
    if u[1] == '1':
        colormap.append('red')
    if u[1] == '2':
        colormap.append('green')
    if u[1] == '3':
        colormap.append('purple')
nx.draw(G, node_color = colormap)
plt.show()
