#! usr/bin/env/python3
# -*- coding : utf8 -*-


liste = []

def levenshtein1(chaine1, chaine2):
    add1 = [0]
    for char2 in chaine2:
        add1.append(char2)
    liste.append(add1)
    for char1 in chaine1:
        add2 = [char1]
        for char in chaine2:
            add2.append(0)
        liste.append(add2)
    for i in range(len(liste)):
        liste[i][0] = i
    for j in range(len(liste[0])):
        liste[0][j] = j
    print(liste)

    for i in range(1, len(liste) + 1):
        for j in range(1, len(liste[0]) + 1):
            if chaine1[i-1] == chaine2[j-1]:
                substitcost = 0
            else:
                substitcost = 1
            liste[i][j] = min(liste[i-1][j] + 1, liste[i][j-1] + 1,
             liste[i-1][j-1] + substitcost)
    return liste[len(chaine1)][len(chaine2)]
            
def iterative_levenshtein(s, t):
    """ 
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t
    """
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution
    return dist[row][col]
