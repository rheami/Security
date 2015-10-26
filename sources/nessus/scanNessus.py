#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

from __future__ import absolute_import
from StringIO import StringIO
import sys
from optparse import OptionParser
from bs4 import BeautifulSoup

def main():

    usage = "usage: %prog file1"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--out", dest="output",
                      help="write report to FILE", metavar="FILE")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error(u"need exactly two input filenames.")

    filename_a = args[0]

    try:
        file = open(filename_a, "r")

    except IOError as e:
        print((sys.stderr, u"Can't open file: %s" % str(e)))
        sys.exit(0)

    soup = BeautifulSoup(file, 'lxml-xml')

    for item in soup.findAll('ReportItem'):
        print(item.get("pluginName"), item.get("port"), item.get("protocol"), item.get("severity"))


# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(0)

if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())