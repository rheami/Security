# coding=utf-8
import sys
from sys import argv
import difflib
import grp
from source.diff_user.user_generator import generateur
#la liste suivante est la manière d'affichier les utilisateurs possible pour un programme

list1 = open("./liste1.txt").readlines()
list2 = open("./liste2.txt").readlines()




listajout = []
listesupp = []
list1='\n'.join(list1)
list2='\n'.join(list2)
print list1
print list2

for line in difflib.unified_diff(list1, list2, fromfile='liste1.txt', tofile='liste2.txt', lineterm='', n=0):

   if line[0]=='-':
    line = line.strip()
    listesupp.append(line[1:])

   if line[0]=='+':
    line = line.strip()
    listajout.append(line[1:])

if  len(listesupp)>1:
    print "liste d'utilisateurs qui sont maintenant present"
    print ", ".join(listesupp[1:])
else:
    print "aucun probleme"