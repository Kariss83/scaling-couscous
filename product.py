#! usr/bin/env/python3
# -*- coding : utf8 -*-


class Product:
    """ This class correspond to the table product in the DB."""


class ProductsRepository:
    """ Managing products."""

    def get_products_by_name(self, name):
        """ Searching for products by name."""

    def get_products_by_nutriscore(self, name):
        """ Searching product by nutriscore."""

    def get_products_by_category(self, name):
        """ Searching product by nutriscore."""


if __name__ == '__main__':

https://fr.openfoodfacts.org/cgi/search.pl?action=process&page_size=1000&json=1
https://fr.openfoodfacts.org/category/{category_name}/{page_number}.json

CREATE TABLE Products (id int, name text, tags text,url text, PRIMARY KEY (id))

activer relative line number