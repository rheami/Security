# coding=utf-8
import difflib
import grp

#la liste suivante est la manière d'affichier les utilisateurs possible pour un programme
import pwd, grp
for p in pwd.getpwall():
     print p[0]


# la liste suivante compare 2 listes et affiche les ajouts et suppression entre 2 listes
list1 = (open("./liste/liste1.txt").readlines())
list2 = open("./liste/liste2.txt").readlines()

list1 = sorted(list1)
list2 = sorted(list2)

listajout = []
listesupp = []
for line in difflib.unified_diff(list1, list2, fromfile='liste1.txt', tofile='liste2.txt', lineterm='', n=0):

   if line[0]=='-':
    line = line.strip()
    listesupp.append(line[1:])

   if line[0]=='+':
    line = line.strip()
    listajout.append(line[1:])

if  len(listajout)>1:
    print "liste d'utilisateurs qui sont maintenant présent"
    print ", ".join(listajout[1:])
if  len(listesupp)>1 :
    print "liste d'utilisateurs qui sont effacés"
    print ", ".join(listesupp[1:])


