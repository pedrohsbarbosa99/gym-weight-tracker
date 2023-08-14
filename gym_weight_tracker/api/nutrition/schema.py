from ninja import Schema


class FoodItem(Schema):
    id: int
    name: str
    kcal: float = None
    kj: float = None
    protein: float = None
    carbohydrates: float = None
    category_name: str
