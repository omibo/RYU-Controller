from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.link import TCLink, Intf
from mininet.cli import CLI
from mininet.node import OVSSwitch

from threading import Timer
from random import randint

from topo1 import Topo1
import time



class Runner1:
    
    def __init__(self):

        self.net = Mininet(topo=Topo1(), link=TCLink, switch=OVSSwitch, host=CPULimitedHost, ipBase='10.0.0.0/8')

    def changeBW(self):
        for link in self.net.links:
            link.intf1.params['bw'] = randint(1, 5)
        Timer(10.0, self.changeBW).start()

    def printBW(self):
        for link in self.net.links:
            print(link.intf1.params['bw']),
        print('\n')
        Timer(5.0, self.printBW).start()
        

    def run(self):
        self.net.start()

        self.changeBW()
        self.printBW()

        # CLI(self.net)
        time.sleep(40)

        self.net.stop()


runner = Runner1()
runner.run()
