from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call


def Topo2():

    def __init__(self):
        Topo.__init__(self)

        c0=self.addController(name='c0',
                        controller=RemoteController,
                            ip= '127.0.0.1',
                        port=6653)

        info( '*** Add switches\n')
        sw1 = self.addSwitch('sw1', cls=OVSKernelSwitch)
        sw2 = self.addSwitch('sw2', cls=OVSKernelSwitch)
        sw3 = self.addSwitch('sw3', cls=OVSKernelSwitch)
        sw4 = self.addSwitch('sw4', cls=OVSKernelSwitch)
        sw5 = self.addSwitch('sw5', cls=OVSKernelSwitch)
        sw6 = self.addSwitch('sw6', cls=OVSKernelSwitch)
        sw7 = self.addSwitch('sw7', cls=OVSKernelSwitch)
        sw8 = self.addSwitch('sw8', cls=OVSKernelSwitch)
        sw9 = self.addSwitch('sw9', cls=OVSKernelSwitch)
        sw10 = self.addSwitch('sw10', cls=OVSKernelSwitch)
        sw11 = self.addSwitch('sw11', cls=OVSKernelSwitch)
        sw12 = self.addSwitch('sw12', cls=OVSKernelSwitch)
        sw13 = self.addSwitch('sw13', cls=OVSKernelSwitch)
        sw14 = self.addSwitch('sw14', cls=OVSKernelSwitch)
        sw15 = self.addSwitch('sw15', cls=OVSKernelSwitch)
        sw16 = self.addSwitch('sw16', cls=OVSKernelSwitch)

        info( '*** Add hosts\n')
        h1 = self.addHost('h1', cls=Host, ip='10.1.0.1',mac='00:00:00:00:00:01', defaultRoute=None)
        h2 = self.addHost('h2', cls=Host, ip='10.1.0.2',mac='00:00:00:00:00:02', defaultRoute=None)
        h3 = self.addHost('h3', cls=Host, ip='10.1.0.3',mac='00:00:00:00:00:03', defaultRoute=None)

        #DC - Chicago
        s1 = self.addHost('s1', cls=Host, ip='10.0.0.1',mac='00:00:00:00:00:11', defaultRoute=None)#file server
        s2 = self.addHost('s2', cls=Host, ip='10.0.0.2',mac='00:00:00:00:00:12', defaultRoute=None)#email server
        s3 = self.addHost('s3', cls=Host, ip='10.0.0.3',mac='00:00:00:00:00:13', defaultRoute=None)#web server
        s4 = self.addHost('s4', cls=Host, ip='10.0.0.4',mac='00:00:00:00:00:14', defaultRoute=None)#backup server
        #DC - NewYork
        s5 = self.addHost('s5', cls=Host, ip='10.0.1.1',mac='00:00:00:00:00:21', defaultRoute=None)#file server
        s6 = self.addHost('s6', cls=Host, ip='10.0.1.2',mac='00:00:00:00:00:22', defaultRoute=None)#email server
        s7 = self.addHost('s7', cls=Host, ip='10.0.1.3',mac='00:00:00:00:00:23', defaultRoute=None)#web server
        s8 = self.addHost('s8', cls=Host, ip='10.0.1.4',mac='00:00:00:00:00:24', defaultRoute=None)#backup server
        #DC - Seattle
        s9 = self.addHost('s9', cls=Host, ip='10.0.2.1',mac='00:00:00:00:00:31', defaultRoute=None)#file server
        s10 = self.addHost('s10', cls=Host, ip='10.0.2.2',mac='00:00:00:00:00:32', defaultRoute=None)#email server
        s11 = self.addHost('s11', cls=Host, ip='10.0.2.3',mac='00:00:00:00:00:33', defaultRoute=None)#web server
        s12 = self.addHost('s12', cls=Host, ip='10.0.2.4',mac='00:00:00:00:00:34', defaultRoute=None)#backup server

        info( '*** Add links\n')
        self.addLink(s1, sw1)
        self.addLink(s2, sw1)
        self.addLink(s3, sw2)
        self.addLink(s4, sw2)
        self.addLink(sw1, sw3, bw=50)
        # self.addLink(sw2, sw4, bw=50)
        self.addLink(sw2, sw3, bw=100)
        self.addLink(sw1, sw4, bw=100)

        self.addLink(s5, sw5)
        self.addLink(s6, sw5)
        self.addLink(s7, sw6)
        self.addLink(s8, sw6)
        self.addLink(sw5, sw7, bw=50)
        # self.addLink(sw6, sw8, bw=50)
        self.addLink(sw6, sw7, bw=100)
        self.addLink(sw5, sw8, bw=100)

        self.addLink(s9, sw9)
        self.addLink(s10, sw9)
        self.addLink(s11, sw10)
        self.addLink(s12, sw10)
        self.addLink(sw9, sw11, bw=50)
        # self.addLink(sw10, sw12, bw=50)
        self.addLink(sw10, sw11, bw=100)
        self.addLink(sw9, sw12, bw=100)

        self.addLink(h1, sw13)
        self.addLink(h2, sw14)
        self.addLink(h3, sw16)

        self.addLink(sw3, sw13, bw=15)
        self.addLink(sw3, sw14, bw=10)
        # self.addLink(sw4, sw14, bw=5)
        # self.addLink(sw7, sw13, bw=15)
        self.addLink(sw7, sw14, bw=20)
        # self.addLink(sw7, sw15, bw=5)
        self.addLink(sw8, sw15, bw=10)
        self.addLink(sw8, sw16, bw=15)
        # self.addLink(sw11, sw14, bw=10)
        self.addLink(sw12, sw15, bw=15)
        # self.addLink(sw12, sw16, bw=10)


        # info( '*** Starting network\n')
        # self.build()
        # info( '*** Starting controllers\n')
        # for controller in self.controllers:
        #     controller.start()

        # info( '*** Starting switches\n')
        # self.get('sw1').start([c0])
        # self.get('sw2').start([c0])
        # self.get('sw3').start([c0])
        # self.get('sw4').start([c0])
        # self.get('sw5').start([c0])
        # self.get('sw6').start([c0])
        # self.get('sw7').start([c0])
        # self.get('sw8').start([c0])
        # self.get('sw9').start([c0])
        # self.get('sw10').start([c0])
        # self.get('sw11').start([c0])
        # self.get('sw12').start([c0])
        # self.get('sw13').start([c0])
        # self.get('sw14').start([c0])
        # self.get('sw15').start([c0])
        # self.get('sw16').start([c0])

        # info( '*** Post configure switches and hosts\n')

        # CLI(self)
        # self.stop()

topos = {'topo2': ( lambda: Topo2() ) }

# if __name__ == '__main__':
#     setLogLevel( 'info' )
#     myNetwork()