#!/bin/bash

rm db.sqlite3
rm -rf ./recipe_api/migrations
python3 manage.py migrate
python3 manage.py makemigrations recipe_api
python3 manage.py migrate recipe_api
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata grocery_subtypes
python3 manage.py loaddata ingredients
python3 manage.py loaddata meal_types
python3 manage.py loaddata recipes
python3 manage.py loaddata ingredients_for_recipes

