from ninja import Schema


class Nutrient(Schema):
    kcal: float = None
    kJ: float = None
    protein: float = None
    carbohydrates: float = None


class Category(Schema):
    id: int
    name: str


class FoodItem(Schema):
    id: int
    name: str
    nutrient: Nutrient
    category: Category
