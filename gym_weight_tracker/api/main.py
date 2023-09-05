from ninja import NinjaAPI

from gym_weight_tracker.api.auth.api import auth_router
from gym_weight_tracker.api.exercise.api import exercise_router
from gym_weight_tracker.api.nutrition.api import nutrition_router
from gym_weight_tracker.api.progression.api import progression_router
from gym_weight_tracker.api.social.api import social_router
from gym_weight_tracker.api.user.api import user_router

api = NinjaAPI(title="Light Weight Baby", version="0.0.3")
api.add_router("/users", user_router, tags=["users"])
api.add_router("/exercises", exercise_router, tags=["exercises"])
api.add_router("", progression_router, tags=["progressions"])
api.add_router("/foods", nutrition_router, tags=["nutrition"])
api.add_router("/social", social_router, tags=["social"])
api.add_router("", auth_router, tags=["auth"])
