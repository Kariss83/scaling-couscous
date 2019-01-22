#! usr/bin/env/python3
# -*- coding : utf8 -*-
"""Connector module documentation
Description:
    This module purposes is to establish connection with the DB though an
    instance of a class called Connector.
    The only taken action is to establish the connection at the creation of the
    instance, so we do it inside the __ini__ method of the class
"""

import records  # https://github.com/kennethreitz/records


class Connector():
    """This Class allow the program to connect to the DB"""

    def __init__(self):
          # using environment variables we get the info needed for the DB
          # connexion
        self.db = records.Database()


if __name__ == "__main__":
    connector = Connector()
