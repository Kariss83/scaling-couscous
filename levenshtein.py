#! usr/bin/env/python3
# -*- coding : utf8 -*-


liste = []

def levenshtein(chaine1, chaine2):
    add1 = [0]
    for char2 in chaine2:
        add1.append(char2)
    liste.append(add1)
    for char1 in chaine1:
        add2 = [char1]
        for char in chaine2:
            add2.append(0)
        liste.append(add2)
    

levenshtein("salut", "coucou")
print(liste)
print(liste[0][5])
        