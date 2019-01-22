#! usr/bin/env/python3
# -*- coding : utf8 -*-
"""Favorite module documentation
Description:
    This module is designed to to interact with the DB in order to either store
    or find stored subsitution couple (initial prod and his substitute).

Note :
    For the storage part --> static method save_fav:
        Using the substitutor class that will store both the product and it's
        substitute the Favorite instance will ask the user if he wants to save
        the result of the substitution. If so it will store a couple of id
        related to both products

    For the finding part --> static method:
        Using only the connector this time, our instance will request the DB to
        first find the couple of saved id then to find the corresponding
        products in the table Products of the DB, and finally displays the
        requested info on each product.
"""

from connector import Connector


class Favorite():
    """This class is used to store and fetch favorites"""

    @staticmethod
    def save_fav(connector, substitutor):
        """This method will safe the favorite into the DB"""
        try:
            choice = input(
                "Voulez vous sauvegarder votre recherche?"
                "Entrez 'oui' on 'non' : ")
            if choice.lower() == "oui":
                # cette reqquêtre devrait enregistrer les id pour retrouver
                # l'intégralité des infos par la suite.
                connector.db.query("""
                    INSERT INTO Favorites(product,substitute)
                    VALUES(:prod, :sub)
                    """,
                    prod=substitutor.prod_choice.name,
                    sub=substitutor.substitute[0].name
                )
                print("Enregistré avec succès!")
            elif choice.lower() == "non":
                pass
            else:
                print("Veuillez entrer une réponse valide svp.")
        except:
            print("Une erreur est survenue lors de l'enregistrement. Désolé.")

    @staticmethod
    def find_old_fav(connector):
        """This methode display all the saved favorites from previous
        searches"""
        # cette méthode devrait plutôt faire apparaitre le numéro de la
        # substitution puis permettre d'entrer dans le détail
        all_fav = connector.db.query("""SELECT * FROM Favorites""")
        if len(all_fav) != 0:
            for fav in all_fav:
                print(fav.product, " peut être remplacé par : ",
                    fav.substitute)
        else:
            print("Nous n'avons pas trouvé de favoris enregistrés")


if __name__ == '__main__':
    connector = Connector()
    favorite = Favorite()
    favorite.find_old_fav(connector)
