#!/bin/bash

# This  script tests the flowmon capabilities
# Author: Malachi Cohen

# In linux we need to be root in order to generate traffic online (in most cases)
su root

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
function communicate_with_malwares {
    ping 98.131.229.2 -W 0 -c 1
    ping 98.131.172.1 -W 0 -c 1
    ping 98.131.132.1 -W 0 -c 1
    ping 96.30.28.181 -W 0 -c 1
    ping 103.31.186.29 -W 0 -c 1
    ping 119.18.61.133 -W 0 -c 1
    ping 176.31.28.226 -W 0 -c 1
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
communicate_with_malwares
# ping google
ping google.com -c 1
print_end "Blacklist"


# DHCP anomaly
# detect increased traffic of DHCP
# Send 100 dhcp request with spoofing client 0.0.0.0
print_start "DHCP increased traffic anomaly"
for i in `seq 1 100`;
    do
            dhcping -r -t 0 -c 0.0.0.0 > /dev/null
            if ! ((i % 10)); then
                echo "$i spoofed DHCP requests were sent."
            fi
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
for i in `seq 1 10`;
    do
            python ARDT.py -l akamai_servers_list.txt -t ${VICTIM} -r ExampleHTTPReq.txt  -n 10 >> /dev/null
            echo "finished $i iterations out of 10!"
    done
cd ..
print_end "reflective DDoS"

# communicate directly with the internet
# access to internet - just ping google.
# -c 1 : only one ping
print_start "connect to internet"
ping google.com -c 1
print_end "connect to internet"


### Port scanning ###
# We do stealth sys scan to check whether flowman detects port scanning
# This should also find icmp type 3 (port unreachable) anomaly

# SYN scan
print_start "SYN port scanning"
sudo nmap -sS ${VICTIM}
print_end "SYN port scanning"

# FIN scan
print_start "FIN port scanning"
sudo nmap -sF ${VICTIM}
print_end "FIN port scanning"

# XMAS scan
print_start "XMAS port scanning"
sudo nmap -sX ${VICTIM}
print_end "XMAS port scanning"

# NULL scan
print_start "NULL port scanning"
sudo nmap -sN ${VICTIM}
print_end "NULL port scanning"

# UDP scan
sudo nmap -sU ${VICTIM}
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
            sudo nc -p 23 -w 0.1 google.com 2> /dev/null
            if ! ((i % 10)); then
                echo "$i telnet requests were sent."
            fi
    done
print_end "Telnet anomaly"

# Checks that flowmon detects large file download, the file is 1.6GB,
# Also should find connectivity to internet
#print_start "large download"
#wget https://archive.ics.uci.edu/ml/machine-learning-databases/00347/1000_train.csv.gz
#rm 1000_train.csv.gz
#print_end "large download"
