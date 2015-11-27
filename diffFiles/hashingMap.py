import hashlib
import os


class exehash(object):
    def __init__(self, dirpath):
        pass

    def locatefile(self):
        pass

    def getmap(self):
        pass




if __name__ == "__main__":
    dirtohash = "/home/cid/SecuriteDev/s-curit-inm5001/diffFiles/txt to hash/"
    maindir = os.path.abspath(dirtohash)
    listedmap = []

    for root, dirs, fnames in os.walk(maindir, topdown=False):
        for i, dir in enumerate(dirs):
            for f in fnames[i]:
                listedmap += [os.path.abspath('{0}/{1}/{2}').format(root, dirs, fnames)]

    for path in listedmap:
        hash = hashlib.md5(open(path, 'rb').read()).digest()
        print('hash: {0} for path: {1}'.format(hash, path))

# todo transformer mon script en commentaire pour mettre en class, et print dans un txt