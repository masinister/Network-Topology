import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product, combinations
from topos import GraphTopo

class Individual():

    def __init__(self, nodes, hosts, edges):
        self.nodes = nodes
        self.hosts = hosts
        self.edges = edges
        self.graph = nx.Graph()
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(self.edges)
        self.isolated_hosts = sum(h in nx.isolates(self.graph) for h in self.hosts)
        self.topo = GraphTopo(self.graph, self.hosts)
        self.fitness = 0
        self.ploss = 0
        self.rtt = 0
        self.counter = 0

    def draw(self, g = 0):
        nx.write_graphml(self.graph, 'img/gen{}.graphml'.format(g))

if __name__ == '__main__':
    I = Individual([0,1],[(0,1)])
    G = I.get_graph()
    print(G.nodes, G.edges)
