from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

# Send DNS request packet sized more than 600 bytes
print "## First anomaly : extra size DNS packet"
extra_payload = (600 * 'z')
sr1(IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="www.google.com")) / extra_payload, verbose=0)

# Send 1000 DNS request packets
print "## Second anomaly : DNS flood"
for i in range(100):
    answer = sr1(IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="www.google.com")), verbose=0)
    if i % 10 == 0:
        print i, "DNS packets were sent"

print i, "DNS packets were sent"
