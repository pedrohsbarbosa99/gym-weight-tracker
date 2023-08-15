# Generated by Django 4.1 on 2023-08-14 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Food",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nutrition.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Nutrient",
            fields=[
                ("kcal", models.FloatField()),
                ("kJ", models.FloatField()),
                ("protein", models.FloatField(null=True)),
                ("carbohydrates", models.FloatField()),
                (
                    "food",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="nutrition.food",
                    ),
                ),
            ],
        ),
    ]
