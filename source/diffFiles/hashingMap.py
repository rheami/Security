import hashlib
import os


class ExeHash(object):
    def __init__(self, dirpath=""):
        self.listedmap = []
        self.hashedpath = {}

        try:
            self.dirpath = dirpath
            self.locatefiles()
        except IOError as e:
            print(e)

        self.setmap()

    def locatefiles(self):
        for dirName, subdirList, fileList in os.walk(self.dirpath):
            for file in fileList:
                self.listedmap += [os.path.join(dirName, file)]

    def setmap(self):
        try:
            for path in self.listedmap:
                hash = hashlib.md5(open(path, 'rb').read()).hexdigest()
                #path =
                self.hashedpath[str(path)] = str(hash)
        except IOError as e:
            pass

# todo

    def getmap(self):
        return self.hashedpath

# todo argparse.ArgumentParser( etc
if __name__ == "__main__":
    dirtohash = "./doc A/"

    test1 = ExeHash(dirtohash)
    hashedmap = test1.getmap()
    print(hashedmap)
