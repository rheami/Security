import pwd, grp
import difflib
listeajout = []
listecree = open("liste2.txt",'w')
class generateur:
        for p in pwd.getpwall():
            p = p[0].strip()
            print p
            listeajout.append(p)
        for p in listeajout :
            listecree.write("%s\n" % p)


