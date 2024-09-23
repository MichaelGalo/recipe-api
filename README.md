# Roll for Recipe Django API

## Overview

Roll for Recipe is a Django API designed to support a cooking application that allows users to manage their recipes, ingredients, and shopping lists. This app aims to simplify meal planning by randomizing recipe selections and generating shopping lists from saved recipes, ultimately saving time for busy individuals who enjoy cooking.

## Problem This App Solved

My wife loves to cook and try new recipes; however, she dislikes having to choose a menu each week before going to the grocery store. This application provides a repository for all her recipes to be stored, updated, or deleted while allowing her to randomize our menu for the week.

## Features

- **User Management**: Create and manage user accounts with authorization tokens for secure access.
- **Recipe Management**: Create, read, update, and delete recipes.
- **Ingredient Management**: Manage ingredients associated with each recipe.
- **Favorites**: Mark recipes as favorites for the ability to roll them.
- **Cuisine Types**: Categorize recipes by different cuisine types.

## Database

The API uses a SQLite3 database to store all data related to users, recipes, ingredients, favorites, and more.

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Django Rest Framework

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/roll-for-recipe.git
   cd roll-for-recipe

2. Create the viritual environment: 

    ```python
    pipenv shell

3. Install dependencies: 

    ```python
    pipenv install

4. Apply migrations:

    ```python
    python manage.py migrate

5. Run the development server:
    ```python
    python manage.py runserver

