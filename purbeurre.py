#! usr/bin/env/python3
# -*- coding : utf8 -*-

import random
from connector import Connector
from test_fetcher import Fetcher
from test_substit import Susbtitutor
from favorite import Favorite
from constants import *
import argparse

class UserInterface():
    """This class will display basic info needed to begiin to run the program"""

    def __init__(self):
        """This method initalize all the variables needed to run the program
        """
        self.choices = False
        connector = Connector()

    def welcome(self):
        """This method print the welcome message"""
        print("""Bienvenue dans le programme PurBeurre.\n
        Vous pouvez taper 0 pour quitter.\n
        Vous pouvez taper 1 pour faire une recherche de substituts.\n
        Vous pouvez taper 2 pour voir les substituts enregistrés sur cette 
        machine.""")
        try:
            self.choices = int(input())
            assert self.choices in (0, 1, 2)
        except ValueError:
            print('Vous devez entrer 0, 1 ou 2!')
        except AssertionError:
            print('Vous devez entrer 0, 1 ou 2!')
    
    def repart(self):
        """This method will analyse the user answer and process to the next 
        part of the program according to it's choice"""
        if self.choices == 0:
            exit()
        elif self.choices == 1:
            UserInterface.make_search()
        else:
            UserInterface.find_search()

    def database_init(self, connector):
        """This method takes all needed actions to create and populate the DB"""
        fetcher = Fetcher()
        fetcher.create_table(connector)
        fetcher.populate_categories(connector)
        for cat in CATEGORIES:
            fetcher.create_crits("categories", "contains", cat, 1000, 
            "unique_scans_n")
            fetcher.request()
            fetcher.populate_products(cat, connector)
        fetcher.populate_tags(connector)
        fetcher.populate_products_has_tags(connector)
        print("""Congratulations, you have initialized the DB! \nYou must now
        launch the program with the option -s or --substitute""")
    
    @classmethod
    def make_search(cls):
        """This method will take all needed actions to make a substitute 
        search"""
        substitutor = Susbtitutor()
        favorite_repository = Favorite()
        substitutor.pick_category(connector)
        substitutor.pick_products(connector)
        substitutor.pick_substitute(connector)
        favorite_repository.save_fav(connector, substitutor)

    @classmethod
    def find_search(cls):
        """This method will take all needed actions to find all saved 
        substitutes"""
        favorite_repository = Favorite()
        favorite_repository.find_old_fav(connector)
        



            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--initalization", action="store_true", 
    help="use this option to initialize the DB at first launch")
    parser.add_argument
    args = parser.parse_args()
    if args.initalization:
        connector = Connector()
        userinterface = UserInterface()
        userinterface.database_init(connector)
    else:
        connector = Connector()
        userinterface = UserInterface()
        userinterface.welcome()
        userinterface.repart()
        

