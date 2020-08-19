#!/usr/bin/python
# -*- coding: utf-8 -*-

from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib import mac
from ryu.topology.api import get_switch, get_link
from ryu.app.wsgi import ControllerBase
from ryu.topology import event, switches
from collections import defaultdict

# switches

switches = []

# mymac[srcmac]->(switch, port)

mymac = {}

# adjacency map [sw1][sw2]->port from sw1 to sw2

adjacency = defaultdict(lambda : defaultdict(lambda : None))


# gets the node for which the minimum distance is stored

def minimum_distance(distance, Q):

    min = float('Inf')

    node = next(iter(Q))

    for v in Q:

        if distance[v] < min:

            min = distance[v]

            node = v

    return node


# gets the shortest path between src and dst

def get_path(
    src,
    dst,
    first_port,
    final_port,
    ):

  # Dijkstra's algorithm

    print('get_path src(switch: {0}, port: {1}) dst(switch: {2}, port: {3})'\
      .format(src, first_port, dst ,final_port))

    distance = {}

    previous = {}

  # initialize all distances with infinity and sets all nodes' parents to None

    for dpid in switches:

        distance[dpid] = float('Inf')

        previous[dpid] = None

  # src node has 0 distance (it's the starting point)

    distance[src] = 0

  # make a copy of switches list since this list will be modified in the next lines

    Q = set(switches)

    # print 'Q=', Q

  # in each iteration, the node with minimum distance is removed from the list and its neighbours are updated

    while len(Q) > 0:

        u = minimum_distance(distance, Q)

        Q.remove(u)

    # iterating over neighbours

        for p in switches:

            if adjacency[u][p] != None:

        # the edge weight

                w = 1

                if distance[u] + w < distance[p]:

          # updating the distance

                    distance[p] = distance[u] + w

          # seting u as p's parent in the found path

                    previous[p] = u

  # this variable is used to store the shortest path

    r = []

  # p and q are used for iterating over the found path

    p = dst

    r.append(p)

    q = previous[p]

  # iterating over the path until it reaches the src

    while q is not None:

        if q == src:

            r.append(q)

            break

        p = q

        r.append(p)

        q = previous[p]

  # the path should be reversed since we reached every node by its child

    r.reverse()

  # if src and dst are the same node, just return it as the found path

    if src == dst:

        path = [src]
    else:

        path = r

  # Now add the ports

    r = []

    in_port = first_port

  # for each pair of consecutive nodes in the found path, add the first node, input port, and output port to the shortest path

    for (s1, s2) in zip(path[:-1], path[1:]):

        out_port = adjacency[s1][s2]

        r.append((s1, in_port, out_port))

        in_port = adjacency[s2][s1]

  # destination is also added to the shortest path

    r.append((dst, in_port, final_port))

    return r

def format_path(p):
  res = ""
  for sw in p:
    res += " {x[0]}->s{x[0]}->{x[0]} ".format(x=sw)
  return res

# initialize the application

class ProjectController(app_manager.RyuApp):

    # set the OpenFlow version

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # initialize the class

    def __init__(self, *args, **kwargs):

        super(ProjectController, self).__init__(*args, **kwargs)

        # initialize mac address table

        self.mac_to_port = {}

        # get results for itself

        self.topology_api_app = self

        # initialize the list of datapaths

        self.datapath_list = []


    # adding entries for the found path to the flow table

    def install_path(
        self,
        p,
        ev,
        src_mac,
        dst_mac,
        ):

        print "install_path: ", format_path(p)

        # print "p=", p, " src_mac=", src_mac, " dst_mac=", dst_mac
      # getting the message from the event

        msg = ev.msg

      # getting the datapath

        datapath = msg.datapath

      # getting the protocol

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

      # iterating over the found path

        for (sw, in_port, out_port) in p:

        # print src_mac,"->", dst_mac, "via ", sw, " in_port=", in_port, " out_port=", out_port
        # specifying a match

            match = parser.OFPMatch(in_port=in_port, eth_src=src_mac,
                                    eth_dst=dst_mac)

        # specifying an action

            actions = [parser.OFPActionOutput(out_port)]

        # getting the corresponding datapath
            datapath = [dp for dp in self.datapath_list if dp.id
                        == sw][0]

        # specifying the instruction

            inst = \
                [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                 actions)]

        # making a flow_mod message

            mod = datapath.ofproto_parser.OFPFlowMod(
                datapath=datapath,
                match=match,
                idle_timeout=0,
                hard_timeout=0,
                priority=1,
                instructions=inst,
                )

        # sending the message

            datapath.send_msg(mod)

    # event handler for receiving a switch features message from a datapath

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        print 'switch_features_handler is called'

      # getting the datapath

        datapath = ev.msg.datapath

      # getting the protocol

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

      # generating an empty match to match all packets

        match = parser.OFPMatch()

      # specifying an action with no buffer with the controller set as the destination

        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                   ofproto.OFPCML_NO_BUFFER)]

      # specifying the instruction

        inst = \
            [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
             actions)]

      # making a flow_mod message

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath,
            match=match,
            cookie=0,
            command=ofproto.OFPFC_ADD,
            idle_timeout=0,
            hard_timeout=0,
            priority=0,
            instructions=inst,
            )

      # sending the message

        datapath.send_msg(mod)

    # event handler for PacketIn

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

      # getting the message from the event

        msg = ev.msg
        
      # compare msg_len and total_len (excepted length)
        if msg.msg_len < msg.total_len:
            print ("packet truncated: only %s of %s bytes", msg.msg_len, msg.total_len)

      # getting the datapath

        datapath = msg.datapath

      # getting the protocol

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

      # getting the input port from the message body

        in_port = msg.match['in_port']

      # making a packet from the message data

        pkt = packet.Packet(msg.data)

      # getting the ethernet frame (Includes source and destination mac address and EtherType)

        eth = pkt.get_protocol(ethernet.ethernet)

      # print "eth.ethertype=", eth.ethertype

      # avoid broadcast from LLDP

        if eth.ethertype == 35020:
            return
      
      # 34525 is a common IPV6 ethertype so if we print it we have a lot of unused logs
      # 2054 is ARP
        # if eth.ethertype == 2054:
        #     print (eth)
    
      # getting destination from the frame (dst is a mac address)

        dst = eth.dst

      # getting source from the frame (src is a mac address)

        src = eth.src

      # getting datapath id from the datapath

        dpid = datapath.id

      # add the datapath id to the mac table

        self.mac_to_port.setdefault(dpid, {})

      # if the source is not present in the mac address table, add it

        if src not in mymac.keys():

            mymac[src] = (dpid, in_port)

        # print "mymac=", mymac

      # if the destination is already learned, decide which port to output the packet, otherwise flood

        if dst in mymac.keys():

        # get the shortest path from source to destination

            print("> From {0}->s{1} to s{2}->{3}"\
              .format(mymac[src][0], mymac[src][1], mymac[dst][0], mymac[dst][1]))

            p = get_path(mymac[src][0], mymac[dst][0], mymac[src][1],
                         mymac[dst][1])

        # add the path to the flow table

            self.install_path(p, ev, src, dst)

        # set the output port to the port set for the starting point of the found path
            out_port = [x[2] for x in p if x[0] == dpid][0]

        else:
            out_port = ofproto.OFPP_FLOOD

      # construct action list

        actions = [parser.OFPActionOutput(out_port)]

        data = None

      # if the message is not buffered, set the data to the message data

        if msg.buffer_id == ofproto.OFP_NO_BUFFER:

            data = msg.data

      # construct packet_out message and send it

        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions,
                                  data=data)

        datapath.send_msg(out)

    # event handler for getting the topology in the beginning

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):

        global switches

      # getting list of switches

        switch_list = get_switch(self.topology_api_app, None)

        switches = [switch.dp.id for switch in switch_list]

      # getting list of datapaths corresponding to the switches

        self.datapath_list = [switch.dp for switch in switch_list]

      # print "self.datapath_list=", self.datapath_list

        print 'switches=', switches

      # getting list of links

        links_list = get_link(self.topology_api_app, None)

        mylinks = [(link.src.dpid, link.dst.dpid, link.src.port_no,
                   link.dst.port_no) for link in links_list]

      # filling the adjacency matrix

        for (s1, s2, port1, port2) in mylinks:

            adjacency[s1][s2] = port1

            adjacency[s2][s1] = port2

            print "s{0}:{1} connected to s{2}:{3}".format(s1, port1, s2, port2)
