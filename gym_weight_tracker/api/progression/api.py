from gym_weight_tracker.account.models import User
from .schema import ProgressionInputSchema, ProgressionSchema
from typing import List
from django.core.handlers.wsgi import WSGIRequest
from gym_weight_tracker.core.models import Exercise, Progression
from django.shortcuts import get_object_or_404
from ninja import Router
from django.db.models import F

progression_router = Router()


@progression_router.get(
    "/exercises/{exercise_id}/progressions",
    response=List[ProgressionSchema],
)
def progressions(request: WSGIRequest, exercise_id: int):
    return Progression.objects.annotate(
        exercise_name=F("exercise__name"),
    ).filter(
        exercise_id=exercise_id,
        user=request.user,
    )


@progression_router.post(
    "/progressions",
    response=ProgressionSchema,
)
def progression_create(request: WSGIRequest, payload: ProgressionInputSchema):
    user = get_object_or_404(User, id=request.user.id)
    exercise = get_object_or_404(Exercise, id=payload.exercise_id)

    progression = Progression(user=user, exercise=exercise, weight=payload.weight)
    progression.save()

    return progression
