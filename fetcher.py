#! usr/bin/env/python3
# -*- coding : utf8 -*-

import records # https://github.com/kennethreitz/records
import requests # https://github.com/kennethreitz/requests



class DbConnector:
    """ This class is used to connect to the DB. """

    def __init__(self):
        self.db = records.Database("mysql+mysqlconnector://student:mot_de_passe@localhost:3306/mysuperdb?charset=utf8mb4")
        self.r = None
        self.j = None
    
    def create_table(self):
        """THis method will create the DB.""" 
        self.db.query('DROP TABLE IF EXISTS Products')
        self.db.query("CREATE TABLE Products (id bigint unsigned, name text, tags text,\
            url text, PRIMARY KEY (id))")
    
    def insert(self):
        pass


    def populate(self, category): #--> 2 responsabilités
        """This method load into db 1000 products of a given category"""
        for page_number in range(1,2): # We need to load 1000 prods so it's 50 pages
            self.r = requests.get(f"https://fr.openfoodfacts.org/category/{category}/{page_number}.json")
            self.j = self.r.json()['products']
            for rec in self.j:
                product_name = rec['product_name_fr']
                product_id_off = rec['_id']
                # nutrition_grade = rec['nutrition_grade_fr'] idem
                # stores = rec['stores'] --> N'existe pas pour tout les produits ?? comment l'intégrer pour ceux qui existent?
                tags = rec['categories_prev_tags']
                url = rec ['url']

                print(f"le nom du produit est : {product_name}, son id est {product_id_off}  et ses tags sont : {tags}")

                self.db.query("INSERT INTO Products(id, name, url, tags) VALUES(:id, :name, :url, :tags)",
                    id=product_id_off, name=product_name, url=url, tags=str(tags))

class Downloader:
    """Download and validate data."""

class DbCreator:
    """Use both of the above to create.""" 
        



if __name__ == '__main__':
    dbconnector = DbConnector()
    dbconnector.create_table()
    dbconnector.populate('viandes')


    