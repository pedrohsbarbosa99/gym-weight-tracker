# Generated by Django 4.2.1 on 2023-05-18 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_progression_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progression',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
