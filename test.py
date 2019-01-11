#! usr/bin/env/python3
# -*- coding : utf8 -*-

import records
import requests
from constants import *


class Connector():
    """This method allow the program to connect to the DB"""

    def __init__(self):
        self.db = records.Database(
            "mysql+mysqlconnector://student:mot_de_passe@localhost"
            ":3306/mysuperdb?charset=utf8mb4")
            #variables d'environnement
            # passer par time pour donner un nom à la DB
            # ou alors le demander à l'utilisateur pour éviter galère


class Fetcher:
    """ This class is used to connect to the DB. """

    def __init__(self):
        self.response = None
        self.json_response = None
        self.criteria = None
        self.urlapi = "https://fr.openfoodfacts.org/cgi/search.pl"
        self.tags_as_set = None
    
    def create_table(self, connector):
        """This method will create the DB.""" 
        connector.db.query('DROP TABLE IF EXISTS Products')
        connector.db.query("""CREATE TABLE Products(
            id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
            nutrigrade VARCHAR(10) NOT NULL,
            name TINYTEXT,
            tags TEXT,
            url TEXT,
            category_id INT NOT NULL REFERENCES category_id,
            stores TEXT NOT NULL,
            PRIMARY KEY (id))"""
        )
        connector.db.query('DROP TABLE IF EXISTS Categories')
        connector.db.query("""CREATE TABLE Categories (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL)"""
        )
        connector.db.query('DROP TABLE IF EXISTS Tags')
        connector.db.query("""CREATE TABLE Tags (
	        id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100)  NOT NULL)"""
        )
        connector.db.query('DROP TABLE IF EXISTS Product_has_tag')
        connector.db.query("""CREATE TABLE Product_has_tag (
	        product_id INT REFERENCES product(id) ON DELETE CASCADE,
            tag_id INT REFERENCES tag(id) ON DELETE CASCADE,
            PRIMARY KEY (product_id, tag_id))"""
        )
    
    def create_crits(self, tagtype_0, tag_contains_0, tag_0, page_size, sort):
        """This method will create a dictionnary in order to request the API"""
        self.criteria = {
            "action" : "process",
            "json" : 1,
            "tagtype_0" : tagtype_0,
            "tag_contains_0" : tag_contains_0,
            "tag_0" : tag_0,
            "page_size" : page_size,
            "sort_by" : sort
        }

    def request(self):
        """This method will reqquest the API on specific criteria"""
        self.response = requests.get(self.urlapi, params=self.criteria)


    def populate_products(self, category, connector):
        """This method will populate the DB with data from the API"""
        self.json_response = self.response.json()['products']
        for rec in self.json_response:
            try:
                category_id_raw = connector.db.query("""SELECT id FROM Categories
                WHERE name = :category""", category=category)
                print(category_id_raw)
                print(category_id_raw[0].id)
                product_name = rec['product_name_fr']
                nutrition_grade = rec['nutrition_grades_tags'][0]
                stores_raw = rec['stores']
                print(stores_raw)
                stores_clean = set(stores_raw.split(','))
                tags_raw = rec['categories_prev_tags']
                tags_clean = set(tags_raw)
                url = rec['url']
                # stocker les magasins égalment.
                if nutrition_grade in ('a', 'b', 'c', 'd', 'e'):
                    connector.db.query("""INSERT INTO Products(id, name, url, 
                    tags, category_id, nutrigrade, stores) VALUES(NULL, :name, 
                    :url, :tags, :category_id, :nutrigrade, :stores)""",
                    name=product_name, url=url, 
                    tags=str(tags_raw), category_id=category_id_raw[0].id, 
                    nutrigrade=nutrition_grade, stores=stores_raw)
            except KeyError:
                print("value missing")

    def populate_categories(self, connector):
        """This method will populate the DB with data from the API"""
        try:
            for cat in CATEGORIES:
                connector.db.query("""INSERT INTO Categories(name) VALUES(
                :name)""", name=cat)
        except KeyError:
            print("Value missing")
    
    def populate_tags(self, connector):
        try:
            unique_tags_set = set()

            all_prod = connector.db.query("""SELECT * FROM Products""")
            for prod in all_prod:
                tags_as_str = prod.tags.split('[')[-1].split((']')[0])
                tags_as_list = tags_as_str[0].split(',')
                for item in tags_as_list:
                    item.replace(' ', '')
                prod_tag_set = set(tags_as_list)
                unique_tags_set = prod_tag_set | unique_tags_set
            for unique_tag in unique_tags_set:
                connector.db.query("""INSERT INTO Tags(name) VALUES(
                    :name)""", name=unique_tag)
        except KeyError:

            pass



if __name__ == '__main__':
    fetcher = Fetcher()
    connector = Connector()
    fetcher.create_table(connector)
    fetcher.create_crits("categories", "contains", "pizza", 1000, 
    "unique_scans_n")
    fetcher.request()
    fetcher.populate_categories(connector)
    fetcher.populate_products("pizza", connector)
    fetcher.populate_tags(connector)
