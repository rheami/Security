#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from libnessus.objects.dictdiffer import DictDiffer
from libnessus.parser import NessusParser

import os
import sys
import argparse

REPORT_ITEM_ = "NessusReportItem::"


class Nessus(object):
    def __init__(self, fileA, fileB):

        self.nessusfileA = fileA
        self.nessusfileB = fileB
        self.nessus_rapportA = NessusParser.parse_fromfile(self.nessusfileA)
        self.nessus_rapportB = NessusParser.parse_fromfile(self.nessusfileB)
        self.set_diff()

    def showDiffDict(self):
        a = {'a': 1, 'b': 1, 'c': 0}
        b = {'a': 1, 'b': 2, 'd': 0}
        return DictDiffer(b, a)

    def get_diff(self):
        self.set_diff()
        return self.diff

    def set_diff(self):
        hosta = self.nessus_rapportA.hosts[0]
        hostb = self.nessus_rapportB.hosts[0]
        self.diff = hostb.diff(hosta)

    def get_unchanged(self):
        # if set diff
        self.set_diff()
        keys = filter(lambda x: x.find(REPORT_ITEM_) != -1, self.diff['unchanged'])
        keys = map(lambda x: x.strip(REPORT_ITEM_), keys)
        vulns_A = {x: self.getInfoA()[x] for x in keys}
        return vulns_A

    def get_added(self):
        # if set diff
        self.set_diff()
        keys = filter(lambda x: x.find(REPORT_ITEM_) != -1, self.diff['added'])
        keys = map(lambda x: x.strip(REPORT_ITEM_), keys)
        vulns_B = {x: self.getInfoB()[x] for x in keys}
        return vulns_B

    def get_removed(self):
        # if set diff
        self.set_diff()
        keys = filter(lambda x: x.find(REPORT_ITEM_) != -1, self.diff['removed'])
        keys = map(lambda x: x.strip(REPORT_ITEM_), keys)
        vulns_A = {x: self.getInfoA()[x] for x in keys}
        return vulns_A

    def get_changed(self):
        # if set diff
        self.set_diff()
        keys = filter(lambda x: x.find(REPORT_ITEM_) != -1, self.diff['changed'])
        keys = map(lambda x: x.strip(REPORT_ITEM_), keys)
        vulns_Changed = {x: str(self.getInfoA()[x]) + " -> " + str(self.getInfoB()[x]) for x in keys}
        return vulns_Changed

    def getInfoA(self):
        host = self.getHostA()
        return self.get_vulns_dict(host)

    def getInfoB(self):
        host = self.getHostB()
        return self.get_vulns_dict(host)

    def get_vulns_dict(self, host):
        vulnList = host.get_report_items
        vulnMap = {}
        for vuln in vulnList:
            str = "port {0} : protocol {1} service {2} severity {3} : {4}".format(vuln.port, vuln.protocol,
                                                                                  vuln.service, vuln.severity,
                                                                                  vuln.get_vuln_info.get('cve'))
            # todo formatter les cve pour qu'il affiche avec des balise <a> {4} </a> pour chaque code cve
            vulnMap[vuln.plugin_id] = str
        return vulnMap
    # todo reception d'action sur le browser

    def getHostA(self):
        return self.nessus_rapportA.hosts[0]

    def getHostB(self):
        return self.nessus_rapportB.hosts[0]

    def afficheremoved(self):
        removed = self.get_removed()
        vA = self.get_VulnsA()
        for s in removed:
            print(vA[s])




EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2





def main():
    # parse args
    parser = argparse.ArgumentParser(
    description='This script parse .nessus file (XML)..')
    parser.add_argument('--firstscan',
                    default="./scan/xp_27.nessus",
                    help="path to a nessusV2 xml")
    parser.add_argument('--secondscan',
                    default="./scan/xp_27B.nessus",
                    help="path to a nessusV2 xml")
    args = parser.parse_args()

    ne = Nessus(args.firstscan, args.secondscan)
    print("added")
    print(ne.get_added())
    print("removed")
    print(ne.get_removed())
    print("changed")
    print(ne.get_changed())
    print("unchanged")
    print(ne.get_unchanged())

# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(EXIT_ERROR)

if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())