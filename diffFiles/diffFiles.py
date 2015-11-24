#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#import simonscript here

import os
import sys
import argparse

#from libnmap.diff import DictDiffer
from libnessus.objects.dictdiffer import DictDiffer


class DiffFiles(object):
    def __init__(self, SourceDir, CompareDir):
        self.sourceDir = SourceDir
        self.compareDir = CompareDir
        #self.filesDictA = simonscript.getFileListWithHash(self.sourceDir)
        self.filesDictA = {'file_a': 1234, 'file_b': 2344, 'file_c': 1235}
        #self.filesDictB = simonscript.getFileListWithHash(self.compareDir)
        self.filesDictB = {'file_a': 1234, 'file_b': 2544, 'file_d': 1235}
        self.set_diff()

    def get_diff(self):
        self.set_diff()
        return self.diff

    def set_diff(self):
        self.diff = DictDiffer(self.filesDictB, self.filesDictA)

    def get_unchanged(self):
        keys = self.diff.unchanged()
        Info = {x: self.getInfoA()[x] for x in keys}
        return Info

    def get_added(self):
        keys = self.diff.added()
        Info = {x: self.getInfoB()[x] for x in keys}
        return Info

    def get_removed(self):
        keys = self.diff.removed()
        Info = {x: self.getInfoA()[x] for x in keys}
        return Info

    def get_changed(self):
        keys = self.diff.changed()
        Info = {x: str(self.getInfoA()[x]) + " ===> " + str(self.getInfoB()[x]) for x in keys}
        return Info

    def getInfoA(self):
        return self.filesDictA

    def getInfoB(self):
        return self.filesDictB


EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2


def main():
    # parse args
    parser = argparse.ArgumentParser(
    description='This script show change between two directory')
    parser.add_argument('--firstDir',
                    default=".",
                    help="path to a directory")
    parser.add_argument('--secondDir',
                    default=".",
                    help="path to a directory")
    args = parser.parse_args()

    diff = DiffFiles(args.firstDir, args.secondDir)

    print("added")
    print(diff.get_added())
    print("removed")
    print(diff.get_removed())
    print("changed")
    print(diff.get_changed())
    print("unchanged")
    print(diff.get_unchanged())

# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(EXIT_ERROR)

if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())
