from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI

from threading import Thread
from random import randint

from topo1 import Topo1



class Runner1:
    
    def __init__(self):

        self.net = Mininet(topo=Topo1(), host=CPULimitedHost, ipBase='10.0.0.0/8')
        hosts = list()

        for i in range(1, 8):
            hosts.append(self.net.get('h' + str(i)))

    def changeBW(self):
        threading.Timer(10.0, self.changeBW).start()
        for link in self.net.link:
            link.intf1.params['bw'] = randint(1, 5)

    def printBW(self):
        threading.Timer(5.0, self.changeBW).start()

        print(hosts[0].cmd('iperf h1 s1'))
        print(hosts[1].cmd('iperf h2 s2'))
        print(hosts[2].cmd('iperf h3 s3'))
        print(hosts[3].cmd('iperf h4 s3'))
        print(hosts[4].cmd('iperf h5 s4'))
        print(hosts[5].cmd('iperf h6 s4'))
        print(hosts[6].cmd('iperf h7 s4'))


    def run(self):
        self.net.start()

        self.changeBW()
        self.printBW()

        CLI(self.net)

        self.net.stop()


runner = Runner1()
runner.run()