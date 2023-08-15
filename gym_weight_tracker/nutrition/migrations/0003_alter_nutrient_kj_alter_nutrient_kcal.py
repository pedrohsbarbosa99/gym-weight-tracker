# Generated by Django 4.1 on 2023-08-14 19:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nutrition", "0002_alter_nutrient_carbohydrates"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nutrient",
            name="kJ",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="nutrient",
            name="kcal",
            field=models.FloatField(null=True),
        ),
    ]