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


@progression_router.get(
    "/last-progessions",
    response=List[ProgressionSchema],
)
def get_last_progressions(request: WSGIRequest):
    progressions = Progression.objects.filter(user=request.user).annotate(
        exercise_name=F("exercise__name"),
    )[:1]

    return progressions


@progression_router.post(
    "/progressions",
    response=ProgressionSchema,
)
def progression_create(request: WSGIRequest, payload: ProgressionInputSchema):
    exercise = get_object_or_404(Exercise, id=payload.exercise_id)

    progression = Progression(
        user=request.user,
        exercise=exercise,
        weight=payload.weight,
    )
    progression.save()

    return progression
