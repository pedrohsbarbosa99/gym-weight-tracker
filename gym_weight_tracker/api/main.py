from .controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI
from gym_weight_tracker.api.exercise.api import exercise_router
from gym_weight_tracker.api.progression.api import progression_router
from gym_weight_tracker.api.user.api import user_router
from gym_weight_tracker.api.nutrition.api import nutrition_router

api = NinjaExtraAPI(title="Light Weight Baby", auth=JWTAuth(), version="0.0.2")
api.add_router("/users", user_router, tags=["users"])
api.add_router("/exercises", exercise_router, tags=["exercises"])
api.add_router("", progression_router, tags=["progressions"])
api.add_router("/foods", nutrition_router, tags=["nutrition"])
api.register_controllers(NinjaJWTDefaultController)
