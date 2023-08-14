from django.db import migrations


def insert_initial_data(apps, schema_editor):
    Category = apps.get_model("nutrition", "Category")
    Food = apps.get_model("nutrition", "Food")
    Nutrient = apps.get_model("nutrition", "Nutrient")

    import json

    with open("gym_weight_tracker/nutrition/migrations/taco.json") as json_data:
        data = json.load(json_data)

        for item in data["data"]:
            category, _ = Category.objects.get_or_create(
                id=item["category"]["id"], defaults={"name": item["category"]["name"]}
            )
            food, _ = Food.objects.get_or_create(
                id=item["id"], defaults={"name": item["name"], "category": category}
            )
            Nutrient.objects.get_or_create(
                food=food,
                defaults={
                    "kcal": item["nutrients"]["kcal"],
                    "kJ": item["nutrients"]["kJ"],
                    "protein": item["nutrients"]["protein"],
                    "carbohydrates": item["nutrients"]["carbohydrates"],
                },
            )


class Migration(migrations.Migration):
    dependencies = [
        ("nutrition", "0003_alter_nutrient_kj_alter_nutrient_kcal"),
    ]

    operations = [
        migrations.RunPython(insert_initial_data),
    ]
