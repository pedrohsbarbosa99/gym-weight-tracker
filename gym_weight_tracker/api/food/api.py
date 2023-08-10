from django.core.handlers.wsgi import WSGIRequest
from ninja import Router

food_router = Router()


@food_router.get("/taco")
def taco(request: WSGIRequest):
    import json

    with open("gym_weight_tracker/api/food/taco.json") as json_data:
        data = json.load(json_data)
        return data
