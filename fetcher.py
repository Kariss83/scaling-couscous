#! usr/bin/env/python3
# -*- coding : utf8 -*-

import records # https://github.com/kennethreitz/records
import requests # https://github.com/kennethreitz/requests
from constants import *



class Fetcher:
    """ This class is used to connect to the DB. """

    def __init__(self):
        self.db = records.Database(
            "mysql+mysqlconnector://student:mot_de_passe@localhost"
            ":3306/mysuperdb?charset=utf8mb4")
        self.response = None
        self.json_response = None
        self.criteria = None
        self.urlapi = "https://fr.openfoodfacts.org/cgi/search.pl"
    
    def create_table(self):
        """THis method will create the DB.""" 
        self.db.query('DROP TABLE IF EXISTS Products')
        self.db.query("CREATE TABLE Products (id SMALLINT UNSIGNED NOT NULL\
         AUTO_INCREMENT, nutrigrade SMALLINT, nutrigradefr SMALLINT, \
         name TINYTEXT, tags TEXT, url TEXT, category TEXT, PRIMARY KEY (id))")
    
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


    def insert(self):
        pass


    def populate(self, category):
        """This method will populate the DB with data from the API"""
        self.json_response = self.response.json()['products']
        for rec in self.json_response:
            try:
                product_name = rec['product_name_fr']
                product_id_off = rec['_id']
                nutrition_grade_fr = rec['nutrition_grade_fr']
                nutrition_grade = rec['nutrition_grade']
                stores = rec['stores']
                tags = rec['categories_prev_tags']
                url = rec ['url']
            except KeyError:
                pass
            self.db.query("INSERT INTO Products(id, name, url, tags,\
             category, nutrigrade, nutrigradefr) VALUES(NULL, :name, :url,\
              :tags, :category, :nutrigrade, :nutrigradefr)",
                name=product_name, url=url, 
                tags=str(tags), category=category, nutrigrade=nutrition_grade, 
                nutrigradefr=nutrition_grade_fr)

class Downloader:
    """Download and validate data."""

class Dbcreator:
    """Use both of the above to create.""" 
        



if __name__ == '__main__':
    fetcher = Fetcher()
    fetcher.create_table()
    fetcher.create_crits("categories", "contains", "pizza", 1000, 
    "unique_scans_n")
    fetcher.request()
    fetcher.populate("pizza")   