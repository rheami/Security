from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from libnessus.objects.dictdiffer import DictDiffer
import sys,argparse,difflib

class Diff_username(object):
    def __init__(self, SourceDir, CompareDir):
        self.filesDictA = []
        self.filesDictB = []

        self.sourceDir = SourceDir
        self.compareDir = CompareDir
        # objet A

        # map A
        self.filesDictA =self.sourceDir

        self.filesDictB = self.compareDir
        # print(self.filesDictB)
        # self.filesDictB = {'file_a': 1234, 'file_b': 2544, 'file_d': 1235}
        self.get_added()
        self.get_removed()

    def get_diff(self):
        self.set_diff()
        return self.diff

    def set_diff(self):
        self.diff = DictDiffer(self.filesDictB, self.filesDictA)







    def get_added(self):
        diff = difflib.ndiff(self.filesDictA, (self.filesDictB))
        Info = ''.join(x[2:] for x in diff if x.startswith('+'))
        Info.rstrip()
        return Info
    def get_removed(self):
        diff = difflib.ndiff(self.filesDictA, (self.filesDictB))
        Info = ''.join(x[2:] for x in diff if x.startswith('-'))
        Info.rstrip()
        return Info



    def getInfoA(self):
        return self.filesDictA.readlines()

    def getInfoB(self):
        return self.filesDictB.readlines()


EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2


def main():
    # parse args
    parser = argparse.ArgumentParser(
    description='This script show change between two directory')
    parser.add_argument('--firstDir',
                    default="liste1.txt",
                    help="path to a directory")
    parser.add_argument('--secondDir',
                    default="liste2.txt",
                    help="path to a directory")
    args = parser.parse_args()

    #args.firstDir = "./doc A/"
    #args.secondDir = "./doc B/"
    # diff = DiffFiles(args.firstDir, args.secondDir)
    file1 = open('./liste2.txt')
    file2 = open('./liste1.txt')
    lines = file1.readlines()
    lines2 = file2.readlines()
    lines = sorted(lines)
    lines2 = sorted(lines2)
    diff =  Diff_username(lines,lines2)
    print("added")
    print (diff.get_added())



# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(EXIT_ERROR)

if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())
