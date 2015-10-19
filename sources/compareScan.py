#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
from __future__ import absolute_import
from StringIO import StringIO
import sys
from optparse import OptionParser
from ndiff import Scan, ScanDiffXML, ScanDiffText, HostDiff
from bs4 import BeautifulSoup

class CompareScan(object):
    def __init__(self, scan_a, scan_b):
        """Create a ScanDiff from the "before" scan_a and the "after"
        scan_b."""
        self.scan_a = scan_a
        self.scan_b = scan_b

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

            print(u"L'indice de différence est: %s" % diff.cost)

        # todo ici

EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2


def usage_error(msg):
    print(u"%s: %s" % (sys.argv[0], msg), file=sys.stderr)
    sys.exit(EXIT_ERROR)


def main():

    usage = "usage: %prog file1 file2"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--out", dest="output",
                      help="write report to FILE", metavar="FILE")

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error(u"need exactly two input filenames.")

    filename_a = args[0]
    filename_b = args[1]

    try:
        scan_a = Scan()
        scan_a.load_from_file(filename_a)
        scan_b = Scan()
        scan_b.load_from_file(filename_b)
    except IOError as e:
        print((sys.stderr, u"Can't open file: %s" % str(e)))
        sys.exit(EXIT_ERROR)

    c = CompareScan(scan_a, scan_b)
    c.test_host_number()
    c.test_date()
    c.test_addresse()
    c.test_hosts()

    f = StringIO()
    scan_diff = ScanDiffXML(scan_a, scan_b, f)
    cost = scan_diff.output()
    xml = f.getvalue()
    #print("---------- xml diff ----------/n")
    #print(xml)
    soup = BeautifulSoup(xml, 'lxml-xml')
    hostdiff = soup.hostdiff
    mapports = {x.get("portid"): x.get("protocol") for x in hostdiff.findAll('port')}
    #print(mapports)
    listport = [x.get("portid") for x in hostdiff.findAll('port')]
    #print(listport)


    for port in soup.hostdiff.findAll('port'):
        print(port.get("portid"), port.get("protocol"), port.state)
        # print(port)

    f.close()

    print(u"L'indice de différence final est: %s" % cost)
    if cost == 0:
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