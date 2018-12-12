#! usr/bin/env/python3
# -*- coding : utf8 -*-

import random


class UserInterface(object):
    """This is the main class of the game, the one that runs the game and load
    every component.
    """

    def __init__(self):
        """ Here we initialize everything that we need to run the program
        """
        self.is_running = False
        self.choice = 0

        #random seed initialization
        random.seed()

    def display_instruction(self, possible_choices, text):
        """ This method will allow the program to display any text asking for
        choices from the user 
        """
        print(text)
        print("Choissisez parmi ces {} paramètres : {}".format(len(possible_choices),possible_choices))
   
   
   def get_user_choice(self):
        """This method will get the user choice and 
        """


if __name__ == "__main__":
    ui = UserInterface()
    ui.display_instruction([0, 1, 2, 'q'], "bienvenue dans le programme de la société pur beurre")
