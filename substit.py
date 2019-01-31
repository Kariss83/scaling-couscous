#! usr/bin/env/python3
# -*- coding : utf8 -*-
"""Substit module documentation
Description:
    This module has the responsibility of finding the substitute to a product
    that has previously been proposed to the user (after having first asked to
    the user to pick a category)

Note:
    The algorythm for finding the best substitute is described here:
    Using only SQL, we will compute for the ingredient picked by the user, the
    number of tags it has in common with all other products that are in the
    same category but with a nutrigrade of b or higher.
    We consider that if products are tagged correctly, the more tags they have
    in common, the more likely they have to be a potential substitute.
"""

import random
from connector import Connector
from constants import CATEGORIES


class Susbtitutor():
    """This class is used to search and propose a substitute"""

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
        """This method will print 5 random products of low nutrigrade
        from the category the user have choosen"""
        print('choississez un aliment à substituer : ')
        # first, we requests the DB for products with bad nutriscore

        # utiliser records et mettre  :
        self.liste_bad = connector.db.query("""SELECT * FROM Products WHERE
            category_id = :category_id AND (nutrigrade IN ('e','d','c'))""",
            category_id=self.cat_choice
        )
        # then we pick 5 random item iin the returned list
        random_list = random.sample(range(1, len(self.liste_bad.all())), 5)
        for i in random_list:
            print(f'{i} : {self.liste_bad[i].name}')
        while True:
            try:
                choice = int(input())
                self.prod_choice = self.liste_bad.all()[choice]
                if choice not in random_list:
                    raise ValueError("Vous devez entrer une valeur valide!")
            except ValueError:
                print('Vous devez entrer une valeur valide!')
            else:
                break
        print('Vous voulez remplacer le produit suivant: ')
        print(self.prod_choice.name)
        print('Plus d\'informations disponibles sur ce produit ici: ')
        print(self.prod_choice.url)
        try:
            print('Vous pouvez trouver ce produit dans le(s) magasin(s)'
            'suivant: ')
            if self.prod_choice.stores:
                print(self.prod_choice.stores)
            else:
                print("Pas de magasins disponibles")
        except AssertionError:
            print("Nous ne savons pas où trouver ce produit")

    def pick_category(self, connector):
        """This method allows the user to pick a category in which he desires
        to find a substitute"""
        print('choose a category : ')
        all_cat = connector.db.query("""SELECT * FROM Categories""")
        cat_list = []
        for cat in all_cat:
            print(cat.id, " ", cat.name)
            cat_list.append(cat.id)
        print()
        while True:
            try:
                self.cat_choice = int(input())
                if self.cat_choice not in cat_list:
                    raise ValueError("Vous devez entrer un numéro valide!")
            except ValueError:
                print("Vous devez entrer un numéro valide!")
            else:
                break
        print(
            f'Vous avez choisi la catégorie : {CATEGORIES[self.cat_choice-1]}')

    def pick_substitute(self, connector):
        """This method compare the number of tag a given product has in common
        with all other products in its category and return the one with most
        tags in common"""
        substitute_cat = CATEGORIES[self.prod_choice.category_id-1]
        self.substitute = connector.db.query("""
        SELECT products.name, products.id, products.url, COUNT(*) FROM Products
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
        GROUP BY products.id
        ORDER BY count(*) DESC""",
        cat_name=substitute_cat,
        prod_id=self.prod_choice.id
        )
        print('voici votre substitut :')
        print(self.substitute[0].name)
        try:
            print("Vous pouvez trouver plus de détails à l'"
            "adresse suivante: ",
            self.substitute[0].url)
        except AttributeError:
            print("Nous ne connaissons pas l'url de ce produit")
        try :
            print('Vous pouvez retrouver ce produit dans les magasins suivants : ',
            self.substitute[0].stores)
        except AttributeError:
            print("Nous ne savons pas où trouver ce produit")


if __name__ == '__main__':
    test = Susbtitutor()
    connector = Connector()
    test.pick_category(connector)
    test.pick_products(connector)
    test.pick_substitute(connector)
