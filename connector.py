#! usr/bin/env/python3
# -*- coding : utf8 -*-

import records # https://github.com/kennethreitz/records


class Connector():
    """This method allow the program to connect to the DB"""

    def __init__(self):
        self.db = records.Database("""mysql+mysqlconnector://student:mot_de_passe@localhost:3306/mysuperdb?charset=utf8mb4""")
            #variables d'environnement
            # passer par time pour donner un nom à la DB
            # ou alors le demander à l'utilisateur pour éviter galère

