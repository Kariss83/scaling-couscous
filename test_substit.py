#! usr/bin/env/python3
# -*- coding : utf8 -*-

import random
from connector import *
from constants import *

class Susbtitutor():


    def __init__(self):
        """This init method create all atributes needed for the substitute"""
        self.test = None
        self.cat_choice = None
        self.prod_choice = None
        self.liste_bad = None
        self.liste_good = None
        self.substitute = None
        self.leven = None
        self.liste_leven = []

    def pick_products(self, connector):
        """This method wiill print 5 random products of low nutrigrade
        from the category the user have choosen"""
        print('choississez un aliment à substituer : ')
        #first, we requests the DB for products with bad nutriscore

        #utiliser records et mettre  :
        self.liste_bad = connector.db.query("""SELECT * FROM Products WHERE
         category_id = :category_id AND (nutrigrade IN ('e','d','c'))""",
          category_id=self.cat_choice)
        #then we pick 5 random item iin the returned list
        random_list = random.sample(range(1,len(self.liste_bad.all())), 5)
        for i in random_list:
            print(f'{i} : {self.liste_bad[i].name}')
        self.prod_choice = self.liste_bad.all()[int(input())]
        print(self.prod_choice)

    def pick_category(self, connector):
        """This method allows the user to pick a category in which he desires
        to find a substitute"""
        print('choose a category : ')
        all_cat = connector.db.query("""SELECT * FROM Categories""")
        for cat in all_cat:
            print(cat.id, " ", cat.name)
        print()
        self.cat_choice = int(input())
        print(f'you have choosen the category : {CATEGORIES[self.cat_choice-1]}')


    def pick_substitute(self, connector):
        """This method will compute for a given product the Levenshtein 
        Distance (LD) with all other products of the same category with a 
        nutrigrade hiigher than b and return a subtite by finding the lowest 
        LD"""
        print(self.prod_choice.category_id)
        print(type(self.prod_choice[0]))
        substitute_cat = CATEGORIES[self.prod_choice.category_id-1]
        self.substitute = connector.db.query("""
        SELECT products.name, COUNT(*) FROM Products
        JOIN Product_has_tag ON Products.id = Product_has_tag.product_id
        JOIN Categories ON  Products.category_id = categories.id
        WHERE 
            categories.name = :cat_name 

            AND products.id != :prod_id

            AND product_has_tag.tag_id IN (
                SELECT tag_id FROM product_has_tag
                WHERE product_id = :prod_id
            )

            AND products.nutrigrade IN ('a', 'b')
        GROUP BY products.name
        ORDER BY count(*) DESC""",
        cat_name=substitute_cat, prod_id=self.prod_choice.id)
        print('voici votre substitut :')
        print(self.substitute[0].name)

        
        





if __name__=='__main__':
    test = Susbtitutor()
    connector = Connector()
    test.pick_category(connector)
    test.pick_products(connector)
    test.pick_substitute(connector)

    