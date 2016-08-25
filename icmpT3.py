import scapy

# set target ip and icmp-data
from scapy.layers.inet import IP, ICMP, sys, send
from scapy.sendrecv import sr

ip_target = sys.argv[1]
data = "flowmon ICMP test"
# define ip and icmp
ip = IP()
icmp = ICMP()
# create ip + icmp parameters
ip.dst = ip_target
icmp.type = 8
icmp.code = 3

for i in range(2):
    send(ip / icmp)
