import difflib
class diffusername:
    file1 = open('./liste1.txt')
    file2 = open('./liste2.txt')
    fileresultat = open ('./listeresultat.txt','w')


    diff = difflib.ndiff(file1.readlines(), file2.readlines())
    delta = ''.join(x[2:] for x in diff if x.startswith('- '))
    print "liste d'utilisateurs qui ont été ajouté"
    print delta
    alpha = ''.join(x[2:] for x in diff if x.startswith('- '))
    print "liste d'utilisateurs qui ont été supprime"
    print alpha
    fileresultat.write("%s\n" % delta)
