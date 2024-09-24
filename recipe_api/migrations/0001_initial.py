# Generated by Django 5.1.1 on 2024-09-24 02:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GrocerySubType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MealType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('grocerySubTypeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_api.grocerysubtype')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('author_favorite', models.BooleanField()),
                ('favorites', models.IntegerField()),
                ('time', models.IntegerField()),
                ('servings', models.IntegerField()),
                ('date', models.DateField()),
                ('meal_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_api.mealtype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientForRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('ingredient_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_api.ingredient')),
                ('recipe_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_api.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_api.recipe')),
                ('user_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]