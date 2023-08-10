from .schema import ProgressionInputSchema, ProgressionSchema, LastProgressionSchema
from typing import List
from django.core.handlers.wsgi import WSGIRequest
from gym_weight_tracker.core.models import Exercise, Progression
from django.shortcuts import get_object_or_404
from ninja import Router
from django.db.models import F, OuterRef, Subquery
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
    progressions = request.user.allowed_progressions().annotate(
        exercise_name=F("exercise__name"),
    )

    return progressions


@progression_router.get(
    "/last-progressions",
    response=List[LastProgressionSchema],
)
def get_progressions(request: WSGIRequest):
    latest_progressions = (
        request.user.allowed_progressions()
        .filter(
            exercise_id=OuterRef("id"),
        )
        .order_by("-created_at")
    )

    queryset = Exercise.objects.annotate(
        last_weight=Subquery(latest_progressions.values("weight")[:1]),
        old_last_weight=Subquery(latest_progressions.values("weight")[1:2]),
        last_date=latest_progressions.values("created_at")[:1],
    ).exclude(last_weight=None)[:10]

    return queryset


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
