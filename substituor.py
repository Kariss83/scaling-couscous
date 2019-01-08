#! usr/bin/env/python3
# -*- coding : utf8 -*-

import random
import purbeurre
from connector import *
from constants import *
from levenshtein import iterative_levenshtein



class Susbtitutor():
    """This class is used to find a substitute to a given product"""

    def __init__(self):
        """This init method create all atributes needed for the substitute"""
        self.test = None
        self.cat_choice = None
        self.prod_choice = None
        self.liste = None
        self.substitute = None
        self.leven = None
        self.liste_leven = []

    def pick_products(self, connector):
        """This method wiill print 5 random products of low nutrigrade
        from the category the user have choosen"""
        print('choississez un aliment à substituer : ')
        #first, we requests the DB for products with bad nutriscore
        self.liste = connector.db.query(f"SELECT * FROM Products WHERE\
         category = '{CATEGORIES[self.cat_choice]}'")
        #then we pick 5 random item iin the returned list
        random_list = random.sample(range(1,len(self.liste.all())), 5)
        for i in random_list:
            print(f'{i} : {self.liste[i].name}')
        self.prod_choice = self.liste.all()[int(input())]
        print(self.prod_choice)

    def pick_category(self):
        """This method allows the user to pick a category in which he desires
        to find a substitute"""
        print('choose a category : ')
        #go through the list of categories in the constants module
        for i,j in enumerate(CATEGORIES):
            print(f'{i} category : {j}')
        self.cat_choice = int(input())
        print(f'you have choosen the category : {CATEGORIES[self.cat_choice]}')

    def pick_substitute(self):
        """This method will compute for a given product the Levenshtein 
        Distance (LD) with all other products of the same category with a 
        nutrigrade hiigher than b and return a subtite by finding the lowest 
        LD"""
        print('voici votre substitut :')
        #computing LD distances with all potential substitutes
        for prod in self.liste:
            tag = prod.tags
            self.leven = iterative_levenshtein(self.prod_choice['tags'], tag)
            self.liste_leven.append((self.leven, prod.id))
        print(min(self.liste_leven))
        #finding the matching product for substitute
        for prod in self.liste:
            if prod.id == min(self.liste_leven)[1]:
                self.substitute = prod
        print(self.substitute)
        print(self.substitute.name)

if __name__ == '__main__':
    test = Susbtitutor()
    connector = Connector()
    test.pick_category()
    test.pick_products(connector)
    test.pick_substitute()

    