#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
from __future__ import absolute_import

import argparse
from StringIO import StringIO
import sys
from optparse import OptionParser
from ndiff import Scan, ScanDiffXML, ScanDiffText, HostDiff
from bs4 import BeautifulSoup
from libnessus.objects.dictdiffer import DictDiffer

class NMapScan(object):
    def __init__(self, fileA, fileB):
        """Create a ScanDiff from the "before" scan_a and the "after"
        scan_b."""

        try:
            scan_a = Scan()
            scan_a.load_from_file(fileA)
            scan_b = Scan()
            scan_b.load_from_file(fileB)
        except IOError as e:
            print((sys.stderr, u"Can't open file: %s" % str(e)))
            sys.exit(EXIT_ERROR)

        f = StringIO()
        scan_diff = ScanDiffXML(scan_a, scan_b, f)
        self.cost = scan_diff.output()
        xml = f.getvalue()
        soup = BeautifulSoup(xml, 'lxml-xml')
        f.close()
        hostdiff = soup.hostdiff
        #map_a = { x.get("portid"): x.get("protocol") for x in hostdiff.findAll('a') }
        #print(map_a)

        ha = hostdiff.findAll('a')
        hb = hostdiff.findAll('b')

        self.port_a = {}
        for a in ha:
            if a.find('port') :
                str = ((a.port.get("portid"), a.port.get("protocol"), a.port.state))
                #print(str)
                self.port_a[a.port.get("portid")] = str

        self.port_b = {}
        for b in hb:
            if b.find('port') :
                str = ((b.port.get("portid"), b.port.get("protocol"), b.port.state))
                #print(str)
                self.port_b[b.port.get("portid")] = str

        self.diff = DictDiffer(self.port_b, self.port_a)

    def getInfoA(self):
        return self.port_a

    def getInfoB(self):
        return self.port_b

    def get_unchanged(self):
        keys = self.diff.unchanged()
        portInfo = {x: self.port_a[x] for x in keys}
        return portInfo

    def get_added(self):
        keys = self.diff.added()
        portInfo = {x: self.port_b[x] for x in keys}
        return portInfo

    def get_removed(self):
        keys = self.diff.removed()
        portInfo = {x: self.port_a[x] for x in keys}
        return portInfo

    def get_changed(self):
        keys = self.diff.changed()
        portInfoa = {x: str(self.port_a[x]) + " -> " + str(self.port_b[x]) for x in keys}
        # todo : ajouter info de b pour voir les changements
        return portInfoa

    def test_host_number(self):
        if len(self.scan_a.hosts) != len(self.scan_b.hosts):
            print("le nombre de host est différent")


    def test_date(self):
        if self.scan_b.end_date <= self.scan_a.end_date :
            print("le deuxieme scan doit avoir lieu apres le scan d'origine", self.scan_a.end_date)


    def test_addresse(self):
        hosta = self.scan_a.hosts[0]
        hostb = self.scan_b.hosts[0]
        if hosta.get_id() != hostb.get_id():
            print(("pas la meme addresse ", hostb.get_id()))

    def test_hosts(self):
        hosta = self.scan_a.hosts[0]
        hostb = self.scan_b.hosts[0]
        diff = HostDiff(hosta, hostb)
        if diff.cost > 0:
            if diff.state_changed:
                print ("state change : %s" % hostb.state)
            if diff.extraports_changed:
                print ("extraports change : %s" % hostb.extraports)
            if diff.os_changed:
                print ("os change : %s" % hostb.os)
            if diff.id_changed:
                print ("id change : %s" % hostb.get_id)

EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2


def usage_error(msg):
    print(u"%s: %s" % (sys.argv[0], msg), file=sys.stderr)
    sys.exit(EXIT_ERROR)


def main():

 # parse args
    parser = argparse.ArgumentParser(
    description='This script parse nmap scan file (XML)..')
    parser.add_argument('--firstscan',
                    default="./scans/scan-origin.xml",
                    help="path to a nmap xml")
    parser.add_argument('--secondscan',
                    default="./scans/scan-212247-101415.xml",
                    help="path to a nmap xml")
    args = parser.parse_args()

    nm = NMapScan(args.firstscan, args.secondscan)
    print("infoa", nm.getInfoA())
    print("infob", nm.getInfoB())
    print("changed : ", nm.get_changed())
    print("added : ",nm.get_added())
    print("removed : ",nm.get_removed())
    print("unchanged : ",nm.get_unchanged())

    print(u"L'indice de différence final est: %s" % nm.cost)
    if nm.cost == 0:
        return EXIT_EQUAL
    else:
        return EXIT_DIFFERENT


# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(EXIT_ERROR)

if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())