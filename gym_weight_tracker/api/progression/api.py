from .schema import ProgressionInputSchema, ProgressionSchema
from typing import List
from django.core.handlers.wsgi import WSGIRequest
from gym_weight_tracker.core.models import Exercise, Progression
from django.shortcuts import get_object_or_404
from ninja import Router
from django.db.models import F
from ninja.pagination import paginate

progression_router = Router()


@progression_router.get(
    "/exercises/{exercise_id}/progressions",
    response=List[ProgressionSchema],
)
@paginate
def get_exercise_progressions(request: WSGIRequest, exercise_id: int):
    return Progression.objects.annotate(
        exercise_name=F("exercise__name"),
    ).filter(
        exercise_id=exercise_id,
        user=request.user,
    )


@progression_router.get(
    "/progessions",
    response=List[ProgressionSchema],
)
@paginate
def get_progressions(request: WSGIRequest):
    progressions = Progression.objects.filter(user=request.user).annotate(
        exercise_name=F("exercise__name"),
    )

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
