#! /usr/bin/env python

from scapy.all import sr1
from scapy.layers.inet import IP, ICMP

# Send extra large ICMP packet
extra_payload = (600 * 'z')
sr1(IP(dst="google.com") / ICMP() / extra_payload, verbose=0)

# flood the net with ICMP
for i in range(100):
    # Log number
    if (i+1) % 10 == 0:
        print i+1, "ICMP packets were sent"

    # Send packet
    sr1(IP(dst="google.com") / ICMP() / extra_payload, verbose=0)



