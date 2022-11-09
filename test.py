from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.util import pmonitor
import random

class TestTopo(Topo):

    def __init__(self, n = 4):
        super(TestTopo, self).__init__()
        switch = self.addSwitch('s0')
        for h in range(n):
            host = self.addHost('h%s' % h)
            self.addLink(host, switch, delay='50ms', max_queue_size = 10)


if __name__ == '__main__':
    seconds = 3
    topo = TestTopo()
    net = Mininet(topo = topo, link = TCLink, controller = OVSController)


    net.start()
    hosts = net.hosts
    popens = {}

    print( "Starting test..." )
    for h in hosts:
        # Start pings
        g = random.choice(hosts)
        popens[h] = h.popen("ping -w 1 -i 0.01 -q %s" % g.IP())
    # Monitor them and print output
    for host, line in pmonitor(popens):
        if host:
            print("<%s>: %s" % (host.name, line))

    net.stop()
