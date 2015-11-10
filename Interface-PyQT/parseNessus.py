#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from math import *
from mimify import repl
from libnessus.parser import NessusParser
from libnessus.objects.dictdiffer import DictDiffer
import os
import sys
import argparse


class Nessus(object):
    def __init__(self, fileA, fileB):

        self.nessusfileA = fileA
        self.nessusfileB = fileB
        self.nessus_rapportA = NessusParser.parse_fromfile(self.nessusfileA)
        self.nessus_rapportB = NessusParser.parse_fromfile(self.nessusfileB)

    def showDiffDict(self):
        a = {'a': 1, 'b': 1, 'c': 0}
        b = {'a': 1, 'b': 2, 'd': 0}
        return DictDiffer(b, a)

    def get_diff(self):
        hosta = self.nessus_rapportA.hosts[0]
        hostb = self.nessus_rapportB.hosts[0]
        return hostb.diff(hosta)

    def get_Vulns(self, host):
        # for host in nrp.hosts: # si plusieurs hosts
        vulnList = host.get_report_items
        vulnMap = {}
        for vuln in vulnList:
            str = "port {0} : protocol {1} service {2} severity {3}".format(vuln.port, vuln.protocol, vuln.service, vuln.severity)
            vulnMap[vuln.plugin_id] = str
        return vulnMap


EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2


def main():
    # parse args
    parser = argparse.ArgumentParser(
    description='This script parse .nessus file (XML)..')
    parser.add_argument('--firstscan',
                    default="./xp_27.nessus",
                    help="path to a nessusV2 xml")
    parser.add_argument('--secondscan',
                    default="./xp_27B.nessus",
                    help="path to a nessusV2 xml")
    args = parser.parse_args()

    ne = Nessus(args.firstscan, args.secondscan)
    print(ne.get_diff())
    print(ne.get_Vulns(ne.nessus_rapportA.hosts[0]))
    print(ne.get_Vulns(ne.nessus_rapportB.hosts[0]))

# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(EXIT_ERROR)

if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())