#!/usr/bin/env python3
# coding=utf-8
import StringIO
import sys

from ndiff import Scan, ScanDiffXML


def test_host_number():
    if len(scan_a.hosts) != len(scan_b.hosts):
        print("le nombre de host est différent")


def test_date():
    if scan_b.end_date <= scan_a.end_date :
        print("le deuxieme scan doit avoir lieu apres le scan d'origine", scan_a.end_date)


def test_addresse():
    hosta = scan_a.hosts[0]
    hostb = scan_b.hosts[0]
    if hosta.get_id() != hostb.get_id():
        print("pas la meme addresse ", hostb.get_id())


if __name__ == '__main__':
    filename_a = "scan-origin.xml"
    #filename_b = "scan-212247-101415.xml"
    filename_b = "test-scans/simple.xml"
    try:
        scan_a = Scan()
        scan_a.load_from_file(filename_a)
        scan_b = Scan()
        scan_b.load_from_file(filename_b)
    except IOError, e:
        print >> sys.stderr, u"Can't open file: %s" % str(e)
        sys.exit(0)

    test_host_number()
    test_date()
    test_addresse()
    f = StringIO.StringIO()
    scan_diff = ScanDiffXML(scan_a, scan_b, f)
    print ("Le 'cost' en différence est de ", scan_diff.output())
    xml = f.getvalue()
    print("---------- xml diff ----------")
    print(xml)
    f.close()

# todo parser le fichier xml