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
                self.hashedpath[str(hash)] = str(path)
        except IOError as e:
            pass

    def getmap(self):
        return self.hashedpath

if __name__ == "__main__":
    dirtohash = "/home/cid/SecuriteDev/s-curit-inm5001/diffFiles/doc A/"

    test1 = ExeHash(dirtohash)
    hashedmap = test1.getmap()
    print(hashedmap)

    # listedmap = []
    # hashedpath = {}
    #
    # for dirName, subdirList, fileList in os.walk(dirtohash):
    #     for fname in fileList:
    #         print(os.path.join(dirName, fname))
    #         listedmap += [os.path.join(dirName, fname)]
    #
    # for path in listedmap:
    #     hash = hashlib.md5(open(path, 'rb').read()).hexdigest()
    #     hashedpath[str(hash)] = str(path)
    #     print('hash: {0} for path: {1}'.format(hash, path))
    #
    # print(hashedpath)
# todo transformer mon script en commentaire pour mettre en class, et print dans un txt