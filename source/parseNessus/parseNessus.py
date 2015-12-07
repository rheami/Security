#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple

import re
from libnessus.objects.dictdiffer import DictDiffer
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
        self._InfoA = {}
        self._InfoB = {}
        self.set_diff()

    def set_diff(self):
        # self._diff = hostb.diff(hosta)
        self.setInfoA()
        self.setInfoB()
        self._diff = DictDiffer(self._InfoB, self._InfoA)

    def get_unchanged(self):
        keys = self._diff.unchanged()
        vulns_A = {x: self.getInfoA()[x] for x in keys}
        return vulns_A

    def get_added(self):
        keys = self._diff.added()
        vulns_B = {x: self.getInfoB()[x] for x in keys}
        return vulns_B

    def get_removed(self):
        keys = self._diff.removed()
        vulns_A = {x: self.getInfoA()[x] for x in keys}
        return vulns_A

    def get_changed(self):
        keys = self._diff.changed()
        vulns_Changed = {x: str(self.getInfoA()[x]) + " -> " + str(self.getInfoB()[x]) for x in keys}
        return vulns_Changed

    def getInfoA(self):
        return self._InfoA

    def setInfoA(self):
        host = self.getHostA()
        self._InfoA = self.get_vulns_dict(host)

    def getInfoB(self):
        return self._InfoB

    def setInfoB(self):
        host = self.getHostB()
        self._InfoB = self.get_vulns_dict(host)

    def get_vulns_dict(self, host):
        vulnList = host.get_report_items
        Vulnerability = namedtuple("Vulnerability", ["plugin_id", "port"])
        vulnMap = {}
        for vuln in vulnList:
            str = "<h4>vulnerability name={}</h4><p> port {} : protocol= {}, service= {}, <b>severity= {}</b></p>".format(
                vuln.plugin_name,
                vuln.port,
                vuln.protocol,
                vuln.service,
                vuln.severity,
                )
            if vuln.get_vuln_info.get('cve'):
                str += ", CVE list: {}".format(vuln.get_vuln_info.get('cve'))

            key = Vulnerability(plugin_id=vuln.plugin_id, port=vuln.port) # key = tuple plugin_id, port
            vulnMap[key] = str
        return vulnMap

    def getHostA(self):
        return self.nessus_rapportA.hosts[0]

    def getHostB(self):
        return self.nessus_rapportB.hosts[0]

    def getMaxSeverity(self):
        host = self.getHostB()
        vulnList = host.get_report_items
        severity_list = [vuln.severity for vuln in vulnList] # real max
        #severity_list = [vuln.severity for vuln in vulnList if ...] # only if vuln in added (maybe higher in unchanged !)
        maxSeverity = max(severity_list)
        return maxSeverity


def showList(info_dict):
        for key in info_dict:
             print("{0} : {1}".format(key, info_dict[key]))

EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2


def main():
    # parse args
    parser = argparse.ArgumentParser(
    description='This script parse .nessus file (XML)..')
    parser.add_argument('--firstscan',
                    default="../scanNessus/rapport-3_gdjv7m.nessus",
                    help="path to a nessusV2 xml")
    parser.add_argument('--secondscan',
                    default="../scanNessus/rapport-1_c9lthb.nessus",
                    help="path to a nessusV2 xml")
    args = parser.parse_args()

    ne = Nessus(args.firstscan, args.secondscan)
    print("liste de A = ", len(ne.getInfoA()))
    showList(ne.getInfoA())
    print("liste de B = ", len(ne.getInfoB()))
    showList(ne.getInfoB())
    i = len(ne.get_added())
    severity = ne.getMaxSeverity()
    print("added = {}, max is {}".format(i, severity))
    showList(ne.get_added())
    print("removed = ", len(ne.get_removed()))
    showList(ne.get_removed())
    print("changed = ", len(ne.get_changed()))
    showList(ne.get_changed())
    print("severity max is {0}".format(ne.getMaxSeverity()))


# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(EXIT_ERROR)


if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())