from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=255)
    kcal = models.FloatField(null=True)
    kJ = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    carbohydrates = models.FloatField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
