# Test Flowmon  
#### This repo is for testing IDS tools.

#### On first time install dependencies:  
~~~~
./dependencies.sh 
~~~~

#### the implemented attacks are:
* blacklist
* DHCP anomaly
* simple DoS
* Amplified DDoS
* Port scanning:
    * SYN
    * FIN
    * NULL
    * XMAS
    * UDP
* SSH dictionary Attack
* TOR traffic simulation
* RDP traffic simulation
* Telnet anomaly
* Large data transfer    

 #### All the above methods will be tested by running ./attacks.sh

# Test learning engines
##### Also, There is test for learning that flowmon clain they have:
* ICMP
* DNS
* DOS
* SMTP  

##### The configuration is found in test_learning/config.py

### in order to run each:  

icmp aggresive: 
~~~~
python test_learning ica  
~~~~
icmp stealth:
~~~~
python test_learning ics  
~~~~
smtp aggresive: 
~~~~
python test_learning sa  
~~~~
smtp stealth: 
~~~~
python test_learning ss  
~~~~
DNS aggresive: 
~~~~
python test_learning da  
~~~~
DNS stealth: 
~~~~
python test_learning ds  
~~~~
DoS aggresive: 
~~~~
python test_learning oa  
~~~~
DoS stealth: 
~~~~
python test_learning os  
~~~~
---
## BUGS / TO FIX:
Sometimes from virtual machine the reflective DDoS does not work.   
To operate it:  
cd reflective_ddos
python ARDT.py -l akamai_servers_list.txt -t ${VICTIM} -r ExampleHTTPReq.txt  -n 10


---
# next we will put it on docker:  
### Docker should be ran as root, so add sudo or command su before

### Docker is a process, which means you should check it's state before work with it and manage it accordingly
sudo service docker <start/stop/status/restart>

### To see all existing containers and their states: 
docker ps -a

### To see all existing images 
docker images

### To run a container from an image: 
docker run -it <id/name> /bin/bash

### To attach to already running container:
docker exec -it <id/name> /bin/bash 

### In order to run the attacks 
docker exec <id/name> /bin/bash -c "cd /home/test_flowmon/ && ./attacks.sh"
