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

1. Create a new user (making sure you use the old authentification plugin) with the command:

```sql
CREATE USER 'name'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

2. Create a new database with the command:

```sql

```

And note the *name* and *password* of the user as you'll need to specify them
later as virtual environnment variables
