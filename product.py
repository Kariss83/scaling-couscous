#! usr/bin/env/python3
# -*- coding : utf8 -*-


class Product:
    """ This class correspond to the table product in the DB."""
    
    def __init__(self):
        """ This method will create the structure of Products in program"""
        self.id = self.db.query("")
        self.name = self.db.query("")
        self.category = self.db.query("")
        self.tags = self.db.query("")
        self.nutrigrade = self.db.query("")
        


class ProductsRepository:
    """ Managing products."""

    def get_products_by_name(self, name):
        """ Searching for products by name."""

    def get_products_by_nutriscore(self, name):
        """ Searching product by nutriscore."""

    def get_products_by_category(self, name):
        """ Searching product by nutriscore."""


if __name__ == '__main__':
    pass