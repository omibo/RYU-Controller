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

def Topo1():

    def __init__(self):
        Topo.__init__(self)

        c0 = self.addController(name='c0',
                            controller=RemoteController,
                            ip='127.0.0.1',
                            port=6653)

        switches = list()
        info('*** Add switches\n')
        for i in range(1, 8):
            switches.append(self.addSwitch('sw'+str(i)))


        hosts = list()
        info('*** Add hosts\n')

        for i in range(1, 9):
            hosts.append(self.addHost('h'+str(i), cls=Host, ip='10.1.0.'+str(i)))


        info('*** Add links\n')
        self.addLink(hosts[0], switches[2])
        self.addLink(hosts[1], switches[2])
        self.addLink(hosts[2], switches[3])
        self.addLink(hosts[3], switches[3])
        self.addLink(hosts[4], switches[5])
        self.addLink(hosts[5], switches[5])
        self.addLink(hosts[6], switches[6])
        self.addLink(hosts[7], switches[6])

        self.addLink(switches[2], switches[1])
        self.addLink(switches[3], switches[1])
        self.addLink(switches[5], switches[4])
        self.addLink(switches[6], switches[4])

        self.addLink(switches[1], switches[0])
        self.addLink(switches[4], switches[0])

topos = {'topo1': ( lambda: Topo1() ) }
    
    # info('*** Starting network\n')
    # net.build()
    # info('*** Starting controllers\n')
    # for controller in net.controllers:
    #     controller.start()

    # info('*** Starting switches\n')
    
    # for i in range(1, len(switches)+1):
    #     net.get('sw'+str(i)).start([c0])

    # info('*** Post configure switches and hosts\n')

    # CLI(net)
    # net.stop()


# if __name__ == '__main__':
#     setLogLevel('info')
#     myNetwork()
