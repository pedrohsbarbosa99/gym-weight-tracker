from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, OuterRef, Subquery
from ninja.pagination import RouterPaginated

from gym_weight_tracker.core.models import Exercise, Progression

from .schema import LastProgressionSchema, ProgressionInputSchema, ProgressionSchema

progression_router = RouterPaginated()


@progression_router.get(
    "/exercises/{exercise_id}/progressions",
    response=List[ProgressionSchema],
)
def get_exercise_progressions(request: WSGIRequest, exercise_id: int):
    return (
        request.user.allowed_progressions()
        .filter(
            exercise_id=exercise_id,
        )
        .annotate(
            exercise_name=F("exercise__name"),
        )
    )


@progression_router.get(
    "/progessions",
    response=List[ProgressionSchema],
)
def get_progressions(request: WSGIRequest):
    progressions = request.user.allowed_progressions().annotate(
        exercise_name=F("exercise__name"),
    )

    return progressions


@progression_router.get(
    "/last-progressions",
    response=List[LastProgressionSchema],
)
def get_last_progressions(request: WSGIRequest):
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
        exercise_id=F("id"),
        exercise_name=F("name"),
    ).exclude(last_weight=None)

    return queryset


@progression_router.post(
    "/progressions",
    response=ProgressionSchema,
)
def progression_create(request: WSGIRequest, payload: ProgressionInputSchema):
    return Progression.objects.create(
        **payload.dict(),
        user=request.user,
    )
