from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call


from mininet.topo import Topo

class Topo1(Topo):

    def __init__(self):
        Topo.__init__(self)

        switches = list()
        info('*** Add switches\n')
        for i in range(1, 5):
            switches.append(self.addSwitch('sw'+str(i)))


        hosts = list()
        info('*** Add hosts\n')

        for i in range(1, 8):
            hosts.append(self.addHost('h'+str(i), cls=Host, ip='10.0.0.'+str(i)))


        info('*** Add links\n')
        self.addLink(hosts[0], switches[0], cls=TCLink, bw=1)
        self.addLink(hosts[1], switches[1], cls=TCLink, bw=2)
        self.addLink(hosts[2], switches[2], cls=TCLink, bw=3)
        self.addLink(hosts[3], switches[2], cls=TCLink, bw=4)
        self.addLink(hosts[4], switches[3], cls=TCLink, bw=5)
        self.addLink(hosts[5], switches[3], cls=TCLink, bw=1)
        self.addLink(hosts[6], switches[3], cls=TCLink, bw=2)

        self.addLink(switches[0], switches[1], cls=TCLink, bw=3)
        self.addLink(switches[0], switches[2], cls=TCLink, bw=4)
        # self.addLink(switches[1], switches[2], cls=TCLink, bw=5)
        self.addLink(switches[2], switches[3], cls=TCLink, bw=1)
        # self.addLink(switches[1], switches[3], cls=TCLink, bw=2)


topos = {'topo1': ( lambda: Topo1() ) }
