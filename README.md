# Docker should be ran as root, so add sudo or command su before

# Docker is a process, which means you should check it's state before work with it and manage it accordingly
sudo service docker <start/stop/status/restart>

# To see all existing containers and their states: 
docker ps -a

# To see all existing images 
docker images

# To run a container from an image: 
docker run -it <id/name> /bin/bash

# To attach to already running container:
docker exec -it <id/name> /bin/bash 

# In order to run the attacks 
docker exec <id/name> /bin/bash -c "cd /home/test_flowmon/ && ./attacks.sh"

# The attacks which currently implemented: 
- communicating with viruses
- DHCP anomaly : spoofed and high rate
- Simple DoS attack
- Reflective DDoS attack
- Port scanning:
	- FIN scan
	- SYN scan
	- XMAS scan
	- NULL scan
- SSH dictionary attack
- RDP attack
- TOR traffic simulation
- RDP traffic simulation 
- Telnet anomaly
