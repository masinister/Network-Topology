import matplotlib.pyplot as plt
import networkx as nx

path = 'img/gen280.graphml'
G = nx.read_graphml(path)
colormap = []
color_dict = {}
pos = {}

for u in G.nodes:
    pos[u] = (int(u[4]),int(u[1]))
    if u[1] == '0':
        colormap.append('blue')
        color_dict[u] = 'blue'
    if u[1] == '1':
        colormap.append('red')
        color_dict[u] = 'red'
    if u[1] == '2':
        colormap.append('green')
        color_dict[u] = 'green'
    if u[1] == '3':
        colormap.append('purple')
        color_dict[u] = 'purple'

print(pos)
# nx.set_node_attributes(G, color_dict, 'color')
print(G.nodes.data())
nx.draw(G, pos, node_color = colormap)
# nx.write_graphml(G, 'img/test.graphml')
plt.show()
