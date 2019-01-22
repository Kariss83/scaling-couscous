#! usr/bin/env/python3
# -*- coding : utf8 -*-
"""module docstring"""
import requests  # https://github.com/kennethreitz/requests
from constants import CATEGORIES
from connector import Connector


class Fetcher:
    """ This class is used to connect to the DB. """

    def __init__(self):
        #  stores api answers
        self.response = None
        # stores api answers in json
        self.json_response = None
        # dictionnary used by requests for api requests
        self.criteria = None
        self.urlapi = "https://fr.openfoodfacts.org/cgi/search.pl"
        # stores all tags in a set ton have the list of all unique tags
        self.tags_as_set = set()

    def create_table(self, connector):
        """This method will create the DB."""
        # creation of table Products
        connector.db.query('DROP TABLE IF EXISTS Products')
        connector.db.query("""CREATE TABLE Products(
            id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
            nutrigrade VARCHAR(10) NOT NULL,
            name TINYTEXT,
            tags TEXT,
            url TEXT,
            category_id INT NOT NULL REFERENCES category_id,
            stores TEXT NOT NULL,
            PRIMARY KEY (id))""")

        # creation of table Categories
        connector.db.query('DROP TABLE IF EXISTS Categories')
        connector.db.query("""CREATE TABLE Categories (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL)""")

        # creation of table Tags
        connector.db.query('DROP TABLE IF EXISTS Tags')
        connector.db.query("""CREATE TABLE Tags (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100)  NOT NULL)""")

        # creation of table Product_has_tag
        connector.db.query('DROP TABLE IF EXISTS Product_has_tag')
        connector.db.query("""CREATE TABLE Product_has_tag (
	    product_id INT REFERENCES product(id) ON DELETE CASCADE,
        tag_id INT REFERENCES tag(id) ON DELETE CASCADE,
        PRIMARY KEY (product_id, tag_id))""")

        # creation of table Favorites
        connector.db.query('DROP TABLE IF EXISTS Favorites')
        connector.db.query("""CREATE TABLE Favorites (
	    id INT PRIMARY KEY AUTO_INCREMENT,
        product VARCHAR(100)  NOT NULL,
        substitute VARCHAR(100) NOT NULL)""")

    def create_crits(self, tagtype_0, tag_contains_0, tag_0, page_size, sort):
        """This method will create a dictionnary in order to request the API"""
        self.criteria = {
            "action":  "process",
            "json":  1,
            "tagtype_0":  tagtype_0,
            "tag_contains_0":  tag_contains_0,
            "tag_0":  tag_0,
            "page_size":  page_size,
            "sort_by":  sort}

    def request(self):
        """This method will reqquest the API on specific criteria"""
        self.response = requests.get(self.urlapi, params=self.criteria)

    def populate_products(self, category, connector):
        """This method will populate the DB with data from the API"""
        self.json_response = self.response.json()['products']
        for rec in self.json_response:
            try:
                # extracts all the needed info of a given product in order to
                # store it in DB
                category_id_raw = connector.db.query("""
                    SELECT id FROM Categories
                    WHERE name = :category""",
                    category=category
                )
                product_name = rec['product_name_fr']
                nutrition_grade = rec['nutrition_grades_tags'][0]
                stores_raw = rec['stores']
                # stores_clean = set(stores_raw.split(','))
                tags_raw = rec['categories_prev_tags']
                self.tags_as_set = set(tags_raw) | self.tags_as_set
                url = rec['url']
                # keeping only products for which we have nutriigrade info
                if nutrition_grade in ('a', 'b', 'c', 'd', 'e'):
                    connector.db.query("""
                        INSERT INTO Products(id, name, url, tags, category_id,
                        nutrigrade, stores) 
                        VALUES(NULL, :name, :url, :tags, :category_id,
                        :nutrigrade, :stores)
                        """,
                        name=product_name, url=url,
                        tags=str(tags_raw),
                        category_id=category_id_raw[0].id,
                        nutrigrade=nutrition_grade,
                        stores=stores_raw
                    )
            # allow us to make sure no product don't have one of the
            # requested info
            except KeyError:
                print("value missing")

    def populate_categories(self, connector):
        """This method will populate the DB with data from the API"""
        try:
            for cat in CATEGORIES:
                connector.db.query("""
                    INSERT INTO Categories(name) VALUES( :name)
                    """,
                    name=cat
                )
        except KeyError:
            print("Value missing")

    def populate_tags(self, connector):
        """ doc """
        try:
            for unique_tag in self.tags_as_set:
                connector.db.query("""
                    INSERT INTO Tags(name) VALUES(:name)""",
                    name=unique_tag
                )
        except KeyError:
            pass

    def populate_products_has_tags(self, connector):
        """ doc """
        try:
            all_prod = connector.db.query("""SELECT * FROM Products""")
            # we take all the products
            for prod in all_prod:
                all_tags = prod.tags.replace('[',
                                             '').replace(']', '').split(',')
                # and for any product we look for the id of its tags
                for tag in all_tags:
                    # then we store couple of prod_id and tag_id
                    try:
                        tag_id = connector.db.query("""
                            SELECT id FROM Tags WHERE name = :name""",
                            name=tag.replace("'", "")
                        )
                        connector.db.query("""
                            INSERT INTO Product_has_tag(product_id, tag_id)
                            VALUES(:prod_id, :tag_id)
                            """,
                            prod_id=prod.id,
                            tag_id=tag_id[0].id
                        )
                    except IndexError:
                        print(tag, "is not a valid tag for this product : ",
                              prod)
        except KeyError:
            pass


if __name__ == '__main__':
    fetcher = Fetcher()
    connectors = Connector()
    fetcher.create_table(connectors)
    fetcher.create_crits("categories", "contains", "pizza", 1000,
                        "unique_scans_n")
    fetcher.request()
    fetcher.populate_categories(connectors)
    fetcher.populate_products("pizza", connectors)
    fetcher.populate_tags(connectors)
    fetcher.populate_products_has_tags(connectors)
