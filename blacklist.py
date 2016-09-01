import os

import wget

# ########################### globals
g_num_of_malware = 10


# ########################### functions
def get_malwares_addresses(content):
    """
    given a file, parse it and return the malware addresses

    :param content: long list of malware addresses
    :return: list of malwares addresses
    """
    # Domains to communicate with
    malware_domains = []
    i = 0
    for line in content:
        # Don't parse comments
        if line[:2] == "##":
            continue
        # Get the malware domain
        malware_domains.append(line.split("\t")[2])

        # Increment i
        i += 1

        # If we have g_num_of_malware break
        if i == g_num_of_malware:
            break

    # Return malware domains
    return malware_domains


def ping_malwares(malware_addresses):
    """
    communicate with malwares addresses given a list of them
    :param malware_addresses: list of malware addresses
    :return: None
    """
    for malware_address in malware_addresses:
        hostname = malware_address
        os.system("ping -c 1 " + hostname)


def communicate_malwares():
    """
    communicate with malwares

    :return: None
    """
    # Link of updated malwares domains list
    url = "http://mirror1.malwaredomains.com/files/domains.txt"

    # Wget it
    filename = wget.download(url)

    # Load all its lines
    with open(filename) as f:
        content = f.readlines()

    # Remove the file
    os.remove(filename)

    # Parse lines and get only domains
    malware_addresses = get_malwares_addresses(content)

    # Communicate with malwares
    ping_malwares(malware_addresses)


if __name__ == '__main__':
    communicate_malwares()
