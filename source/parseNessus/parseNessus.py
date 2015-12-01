#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from libnessus.parser import NessusParser
import sys
import argparse

REPORT_ITEM_ = "NessusReportItem::"

class Nessus(object):
    def __init__(self, fileA, fileB):
        self.nessusfileA = fileA
        self.nessusfileB = fileB
        self.nessus_rapportA = NessusParser.parse_fromfile(self.nessusfileA)
        self.nessus_rapportB = NessusParser.parse_fromfile(self.nessusfileB)
        self._diff = None
        self.set_diff(self.nessus_rapportA.hosts[0], self.nessus_rapportB.hosts[0])

    def get_diff(self):
        return self._diff

    def set_diff(self, hosta, hostb):
        self._diff = hostb.diff(hosta)

    diff = property(get_diff, set_diff, "I'm the 'diff' property.")

    def get_unchanged(self):
        keys = [key.strip(REPORT_ITEM_) for key in self._diff['unchanged'] if key.find(REPORT_ITEM_) != -1]
        vulns_A = {x: self.getInfoA()[x] for x in keys}
        return vulns_A

    def get_added(self):
        keys = [key.strip(REPORT_ITEM_) for key in self._diff['added'] if key.find(REPORT_ITEM_) != -1]
        vulns_B = {x: self.getInfoB()[x] for x in keys}
        return vulns_B

    def get_removed(self):
        keys = [key.strip(REPORT_ITEM_) for key in self._diff['removed'] if key.find(REPORT_ITEM_) != -1]
        vulns_A = {x: self.getInfoA()[x] for x in keys} # todo keys = tupple plugginid, port
        return vulns_A

    def get_changed(self):
        keys = [key.strip(REPORT_ITEM_) for key in self._diff['changed'] if key.find(REPORT_ITEM_) != -1]
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
            str = "vuln info={}, port {} : protocol= {}, service= {}, severity= {}, CVE list: {}".format(
                vuln.plugin_name, # nom de la vulnerabilite
                vuln.port,
                vuln.protocol,
                vuln.service,
                vuln.severity,
                vuln.get_vuln_info.get('cve'))
            # todo formatter les cve pour qu'il affiche avec des balise <a> {4} </a> pour chaque code cve
            vulnMap[vuln.plugin_id] = str
        return vulnMap
    # todo reception d'action sur le browser

    def getHostA(self):
        return self.nessus_rapportA.hosts[0]

    def getHostB(self):
        return self.nessus_rapportB.hosts[0]

    def getMaxSeverity(self):
        vulnMap = self.getSeverityDict()

        keys = [key.strip(REPORT_ITEM_) for key in self._diff['added'] if key.find(REPORT_ITEM_) != -1]
        keys += [key.strip(REPORT_ITEM_) for key in self._diff['changed'] if key.find(REPORT_ITEM_) != -1]

        maxSeverity = 0
        for x in keys:
            y = int(vulnMap[x])
            maxSeverity = max(maxSeverity, y)
            # if maxSeverity == 4 break !
        return maxSeverity

    def getSeverityDict(self):
        vulnList = self.getHostB().get_report_items
        vulnMap = {}
        for vuln in vulnList:
            vulnMap[vuln.plugin_id] = vuln.severity
        return vulnMap


EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2


def main():
    # parse args
    parser = argparse.ArgumentParser(
    description='This script parse .nessus file (XML)..')
    parser.add_argument('--firstscan',
                    default="./scanNessus/xp_27.nessus",
                    help="path to a nessusV2 xml")
    parser.add_argument('--secondscan',
                    default="./scanNessus/xp_27B.nessus",
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
    print("severity max is {0}".format(ne.getMaxSeverity()))

# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(EXIT_ERROR)

if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())