from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F
from ninja import Query
from ninja.pagination import RouterPaginated
from ninja_jwt.authentication import JWTAuth

from gym_weight_tracker.api.nutrition.filters import FoodFilterSchema
from gym_weight_tracker.api.nutrition.schema import FoodItem
from gym_weight_tracker.nutrition.models import Food

nutrition_router = RouterPaginated(auth=JWTAuth())


@nutrition_router.get("/taco", response=List[FoodItem])
def get_taco(
    request: WSGIRequest,
    filters: FoodFilterSchema = Query(...),
):
    foods = Food.objects.annotate(category_name=F("category__name"))
    foods = filters.filter(foods)
    return foods
