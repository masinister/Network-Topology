import matplotlib.pyplot as plt
import networkx as nx
import math

path = 'img/gen50.graphml'
G = nx.read_graphml(path)
colormap = []
color_dict = {}
pos = {}

for u in G.nodes:
    layer = int(u[1])
    num = int(u[4])
    # pos[u] = (4 + math.sin(num)*(4-layer)**2, 4 + math.cos(num)*(4-layer)**2)
    pos[u] = (num, layer)
    if layer == 0:
        colormap.append('blue')
        color_dict[u] = 'blue'
    if layer == 1:
        colormap.append('red')
        color_dict[u] = 'red'
    if layer == 2:
        colormap.append('green')
        color_dict[u] = 'green'
    if layer == 3:
        colormap.append('purple')
        color_dict[u] = 'purple'

print(pos)
# nx.set_node_attributes(G, color_dict, 'color')
print(G.nodes.data())
nx.draw(G, pos, node_color = colormap)
# nx.write_graphml(G, 'img/test.graphml')
plt.show()
