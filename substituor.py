#! usr/bin/env/python3
# -*- coding : utf8 -*-

import random
import purbeurre
from connector import *
from constants import *
from levenshtein import iterative_levenshtein



class Test():

    def __init__(self):
        self.test = None
        self.cat_choice = None
        self.prod_choice = None
        self.liste = None
        self.substitute = None
        self.leven = None
        self.liste_leven = []

    def pick_products(self, connector):
        print('choississez un aliment à substituer : ')
        self.liste = connector.db.query(f"SELECT * FROM Products WHERE\
         category = '{CATEGORIES[self.cat_choice]}'")
        random_list = random.sample(range(1,len(self.liste.all())), 5)
        for i in random_list:
            print(f'{i} : {self.liste[i].name}')
        self.prod_choice = self.liste.all()[int(input())]
        print(self.prod_choice)


    def pick_category(self):
        print('choose a category : ')
        for i,j in enumerate(CATEGORIES):
            print(f'{i} category : {j}')
        self.cat_choice = int(input())
        print(f'you have choosen the category : {CATEGORIES[self.cat_choice]}')


    def pick_substitute(self):
        print('voici votre substitut :')
        for prod in self.liste:
            tag = prod.tags
            self.leven = iterative_levenshtein(self.prod_choice['tags'], tag)
            self.liste_leven.append((self.leven, prod.id))
        print(min(self.liste_leven))
        for prod in self.liste:
            if prod.id == min(self.liste_leven)[1]:
                self.substitute = prod
        print(self.substitute)
        print(self.substitute.name)





if __name__ == '__main__':
    test = Test()
    connector = Connector()
    test.pick_category()
    test.pick_products(connector)
    test.pick_substitute()

    