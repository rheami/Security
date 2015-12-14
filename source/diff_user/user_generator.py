import pwd, grp
import difflib
listeajout = []
listecree = open("liste2.txt",'w')
class generateur:
        for user in pwd.getpwall():
            user= user[0].strip()
            listeajout.append(user)
        for user in listeajout :
            listecree.write("{}\n".format(user))



