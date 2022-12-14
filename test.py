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

def testone(topo, interval = 0.1):
    net = Mininet(topo = topo, link = TCLink, controller = OVSController)
    net.start()
    hosts = net.hosts
    popens = {}

    # print( "Starting test..." )
    for h in hosts:
        for g in hosts:
            if g != h:
                popens[(h,g)] = h.popen("sudo ping -w 1 -i {} -q {}".format(interval, g.IP()))

    # Monitor them and print output
    loss = 0
    rtt = 0
    conns = 0
    for conn, line in pmonitor(popens):
        if conn:
            # print("<%s, %s>: %s" % (conn[0].name, conn[1].name, line))
            type, v = parse_ping(line)
            if type == 'packets':
                sent = float(v[0])
                lost = float(v[1])
                loss += lost/sent
                if lost != sent:
                    conns += 1
            if type == 'rtt':
                rtt += v[1]
    net.stop()
    return loss, rtt, conns

if __name__ == '__main__':
    seconds = 3
    topo = TestTopo()
    print(testone(topo))
