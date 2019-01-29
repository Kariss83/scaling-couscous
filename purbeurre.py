#! usr/bin/env/python3
# -*- coding : utf8 -*-
"""Main file of the program
Description:
    This file define the UserInterface class that is responsible for printing
    to the user the choices he has to make and stores its answers in order to
    make him proceed to the good part of the program (finding a substitute or
    find saved substitutes).

Note:
    With the welcome method the instance of UserInterface will present the user
    it's first choices and stores its answer.
    With the repart method the instance will analyse the answer and launch the
    method corresponding to the user's input
    With the database_init method the instance will initialize an instance of
    Fetcher (in fetcher.py module) in order to both create the DB and its table
    and populate them
    With the make_search method, the instance will initialize an instance of
    Substitutor (substit.py module) and an instance of Favorite (favorite.py
    module) in order let the other search a substitute and save it in the DB
    and then send back to the welcome method.
    With the find_search method, the instance will initialize an instance of
    Favorite (favorite.py module) in order to print all the saved previous
    substitutes.

Options:
    -i, --initalization : launch the program for the first time with this
        option in order to prepare the DB.


"""

from connector import Connector
from fetcher import Fetcher
from substit import Susbtitutor
from favorite import Favorite
from constants import CATEGORIES
import argparse  # https://docs.python.org/3/library/argparse.html


class UserInterface():
    """This class will display basic info needed to begin to run the program"""

    def __init__(self):
        """This method initalize all the variables needed to run the program
        """
        # stores the user's inputs
        self.choices = False

    def welcome(self):
        """This method print the welcome message"""
        print("""Bienvenue dans le programme PurBeurre.\n
        Vous pouvez taper 0 pour quitter.\n
        Vous pouvez taper 1 pour faire une recherche de substituts.\n
        Vous pouvez taper 2 pour voir les substituts enregistrés sur cette
        machine.""")
        # allows us to repeat the process until a valid input is given
        while True:
            try:
                self.choices = int(input())
                if self.choices not in (0, 1, 2):
                    raise ValueError("Vous devez entrer 0, 1 ou 2!")
            except ValueError:
                print('Vous devez entrer 0, 1 ou 2!')
            else:
                break
        self.repart()

    def repart(self):
        """This method will analyse the user answer and process to the next
        part of the program according to it's choice"""
        if self.choices == 0:
            exit()
        elif self.choices == 1:
            self.make_search()
        else:
            self.find_search()

    @staticmethod
    def database_init(connector):
        """This method takes needed actions to create and populate the DB"""
        # We use the fetcher to create then populate all DB tables
        fetcher = Fetcher()
        fetcher.create_table(connector)
        fetcher.populate_categories(connector)
        # we populate products table categories by categories
        for cat in CATEGORIES:
            fetcher.create_crits("categories", "contains", cat, 1000,
                "unique_scans_n"
            )
            fetcher.request()
            fetcher.populate_products(cat, connector)
        fetcher.populate_tags(connector)
        fetcher.populate_products_has_tags(connector)
        print("Congratulations, you have initialized the DB! \nYou must now "
            "launch the program without option"
        )

    def make_search(self):
        """This method will take all needed actions to make a substitute
        search"""
        substitutor = Susbtitutor()
        favorite_repository = Favorite()
        # offering choice between categories
        substitutor.pick_category(connector)
        # offering choice between five random ingredients in a given category
        substitutor.pick_products(connector)
        substitutor.pick_substitute(connector)
        favorite_repository.save_fav(connector, substitutor)
        self.welcome()

    def find_search(self):
        """This method will take all needed actions to find all saved
        substitutes"""
        favorite_repository = Favorite()
        favorite_repository.find_old_fav(connector)
        self.welcome()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--initalization", action="store_true",
        help="use this option to initialize the DB at first launch"
    )
    args = parser.parse_args()
    if args.initalization:  # in this case we just initialize the DB
        connector = Connector()
        userinterface = UserInterface()
        userinterface.database_init(connector)
    else:  # in this case, normal use of the program
        connector = Connector()
        userinterface = UserInterface()
        userinterface.welcome()
