from django.core.handlers.wsgi import WSGIRequest
from ninja.pagination import RouterPaginated
from gym_weight_tracker.api.nutrition.filters import FoodFilterSchema
from gym_weight_tracker.api.nutrition.schema import FoodItem
from gym_weight_tracker.nutrition.models import Food
from ninja import Query
from typing import List

nutrition_router = RouterPaginated()


@nutrition_router.get("/taco", response=List[FoodItem])
def get_taco(
    request: WSGIRequest,
    filters: FoodFilterSchema = Query(...),
):
    foods = Food.objects.all()
    foods = filters.filter(foods)
    return foods
