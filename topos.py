from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.util import pmonitor
import networkx as nx
from test import testone


class GraphTopo(Topo):

    def __init__(self, G, H):
        super(GraphTopo, self).__init__()
        hosts = {}
        switches = {}
        for i, h in enumerate(H):
            hosts[h] = self.addHost('h%s' % i)

        for i, g in enumerate(G.nodes):
            if g not in H:
                switches[g] = self.addSwitch('s%s' % i)

        for u, v in G.edges:
            print(u,v)
            if u in H:
                self.addLink(hosts[u], switches[v], delay='20ms', max_queue_size = 10)
            elif v in H:
                self.addLink(switches[u], hosts[v], delay='20ms', max_queue_size = 10)
            else:
                self.addLink(switches[u], switches[v], delay='20ms', max_queue_size = 10)

if __name__ == '__main__':
    graph = nx.grid_graph([3,3])
    hosts = [(0,0),(0,2),(2,0),(2,2)]
    topo = GraphTopo(graph, hosts)
    net = Mininet(topo = topo, link = TCLink, controller = OVSController)
    testone(net)
