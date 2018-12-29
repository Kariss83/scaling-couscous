#!/usr/bin/env python3
# coding: utf-8

import json # https://docs.python.org/3/library/json.html
import requests # https://github.com/kennethreitz/requests
import records # https://github.com/kennethreitz/records

# randomuser.me generates random 'user' data (name, email, addr, phone number, etc)
r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?categories=viandes&page_size=20&json=1')
j = r.json()['results']


# records will create this db on disk if 'users.db' doesn't exist already
db = records.Database("mysql+mysqlconnector://student2:mot_de_passe@localhost:3306/mysuperdb?charset=utf8mb4")

db.query('DROP TABLE IF EXISTS Persons')
db.query('CREATE TABLE Persons (id int, fname text, lname text, email text, PRIMARY KEY (id))')

for rec in j:
    user = rec['user']
    name = user['name']

    key = user['registered']
    fname = name['first']
    lname = name['last']
    email = user['email']
    db.query('INSERT INTO persons (id, fname, lname, email) VALUES(:id, :fname, :lname, :email)',
            id=key, fname=fname, lname=lname, email=email)

rows = db.query('SELECT * FROM Persons')
print(rows.export('csv'))