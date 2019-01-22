# scaling-couscous

This program proposes the user a subsitute for any ingredient that he searches
using the OpenFoodFact API

## Use scenario

You, as a good citizen of the world, have decided that you cannot keep eating
junk food that are not only bad for your health but also for the planet.
You have taken the decision to change all of that.
When you launch the program you have three options:

0. You can quit the program,

1. You can ask the program "to choose a substitute",

2. You can see your saved substitutes from previous searches.

### Should you choose to search for a substitute

The system will ask you to select the category of ingredient your want to substitute.
It will display all disponible categories with an associated number.
Once you have choosen the category, the system will ask you to select the ingredient
while once again proposing different ingredients inside the choosen category.
Finally, the system will print out a substitute ingredient and propose you to
save the result of this susbtitution.
After that, you'll be sent back to the initial screen.

### Should you choose to search a saved subtitute

The system will print to you the list of your previous saved search. You'll be
able to see the initial product's name, url and disponible stores, and the same
infos for the substitute.
After that, you'll be sent back to the initial screen.

## How to run this program

To get this program you'll need to have installed MySQL on your machine.
Preferably MySQL5.7 as the new Authentication plugin 'caching_sha2_password'
is not supported yet by one of the module used in this program.

Then you'll have to do the following steps:

1. Create a new user (making sure you use the old authentification plugin) 
    with the command:

```sql
CREATE USER 'user_name'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

And note the *name* and *password* of the user as you'll need to specify them
later as virtual environnment variables

2. Create a new database with the command:

```sql
CREATE DATABASE db_name;
```

Once again, note the *db_name* as we will use it a bit later as a virtual
environment variable.

3. Grant your user privileges on the DB you just created using the following command:

```sql
GRANT ALL PRIVILEGES ON db_name.* TO 'user_name'@'localhost';
```

4. Get the project on your machine by running this command:

```bash
git clone https://github.com/Kariss83/scaling-couscous.git
```

5. Put yourself in the directory and create a .env file containing your infos
    (here is what your file should look like):

```
# We need in here the name of the DB created to run the project
# And the credentials to access it in order to make connection to the DB

# url of db connection
DATABASE_URL = mysql+mysqlconnector://your_user_name:your_user_password@localhost:3306/your_db_name?charset=utf8mb4
```

What you have to do is replace *your_user_name:your_user_password* by the info
you used in step 1 and replace *your_db_name* by the info you used in step 2.

6. If you don't use pipenv yet you'll have to install it by running:

```bash
python -m pip install pipenv
```

Then, use it to install of the needed modules by running:

```bash
pipenv install
```

7. You'll have then to run the program a first time to initialize the db:

Start the virutalenv by running:

```bash
pipenv shell
```

Then when you are using it launch the program by running:

```bash
python purbeurre.py -i
```

The *-i* option will initialize the DB in order to be able to run the program.
Watch out if you don't use this option the first time your program won't run!!!

After the installation of the DB is completed you can launch the program using
the following command:

```bash
python purbeurre.py
```

## Troubleshooting

If you have trooble using this program don't hesitate to ask for help here on GitHub.

## Thanks

Thanks to Kenneth Reitz for it's amazing [records module](https://github.com/kennethreitz)! 