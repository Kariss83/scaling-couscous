#! usr/bin/env/python3
# -*- coding : utf8 -*-
"""module docstring"""

from connector import Connector


class Favorite():
    """This class is used to store and fetch favorites"""

    def save_fav(self, connector, substitutor):
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

    def find_old_fav(self, connector):
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
