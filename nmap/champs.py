#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import
import subprocess


# the server to test
class Server(object):
    def __init__(self, ip, hostname):
        self.ip = ip
        self.hostname = hostname

    def set_ip(self, ip):
        self.ip = ip

    def set_hostname(self, hostname):
        self.hostname = hostname

    def ping(self, ip_addr):
        print("Pinging %s from %s (%s)" % (ip_addr, self.ip, self.hostname))
        #subprocess.call(["nping", ip_addr])

if __name__ == '__main__':

    filename = "commandes.txt"
    fileCommands = open(filename, 'r')
    commande = fileCommands.readline().rstrip() # changer pour une liste
    subprocess.call(commande, shell=True)
    commande = fileCommands.readline().rstrip() # changer pour une liste
    subprocess.call(commande, shell=True)
    fileCommands.close()

    server = Server('192.168.1.20', 'nom')
    server.ping('192.168.1.15')



