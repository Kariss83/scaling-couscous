#! usr/bin/env/python3
# -*- coding : utf8 -*-
"""module docstrings"""

import records  # https://github.com/kennethreitz/records


class Connector():
    """This method allow the program to connect to the DB"""

    def __init__(self):
          # using environment variables we get the info needed for the DB
          # connexion
        self.db = records.Database()


if __name__ == "__main__":
    connector = Connector()
