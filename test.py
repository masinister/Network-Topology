from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.util import pmonitor
import random
from utils import parse_ping

class TestTopo(Topo):

    def __init__(self, n = 4):
        super(TestTopo, self).__init__()
        switch = self.addSwitch('s0')
        for h in range(n):
            host = self.addHost('h%s' % h)
            self.addLink(host, switch, delay='10ms', max_queue_size = 10)

def testone(net):
    net.start()
    hosts = net.hosts
    popens = {}

    print( "Starting test..." )
    for h in hosts:
        # Start pings
        # g = random.choice(hosts)
        for g in hosts:
            popens[(h,g)] = h.popen("ping -c 100 -W 0.5 -i 0.01 -q {}".format(g.IP()))

    # Monitor them and print output
    sent = 0
    lost = 0
    for conn, line in pmonitor(popens):
        if conn:
            # print("<%s, %s>: %s" % (conn[0].name, conn[1].name, line))
            type, v = parse_ping(line)
            if type == 'packets':
                sent += v[0]
                lost += v[1]
    net.stop()
    print(sent, lost)

if __name__ == '__main__':
    seconds = 3
    topo = TestTopo()
    net = Mininet(topo = topo, link = TCLink, controller = OVSController)
    testone(net)
