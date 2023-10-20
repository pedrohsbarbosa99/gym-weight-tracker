from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404
from ninja import Query
from ninja.pagination import RouterPaginated

from gym_weight_tracker.core.models import Exercise

from .filters import ExerciseFilterSchema
from .schema import ExerciseInputSchema, ExerciseSchema

exercise_router = RouterPaginated()


@exercise_router.get("", response=List[ExerciseSchema])
def exercises(
    request: WSGIRequest,
    filters: ExerciseFilterSchema = Query(...),
):
    exercises = Exercise.objects.all()
    exercises = filters.filter(exercises)
    return exercises


@exercise_router.patch("/{exercise_id}")
def update_exercise(request, exercise_id: str, payload: ExerciseInputSchema):
    Exercise.objects.filter(pk=exercise_id).update(
        **payload.dict(exclude_none=True)
    )
    return {"Success": True}


@exercise_router.post("", response=ExerciseSchema)
def create_exercise(request, payload: ExerciseInputSchema):
    return Exercise.objects.create(**payload.dict())


@exercise_router.delete("/{exercise_id}")
def delete_exercise(request, exercise_id: str):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    exercise.delete()
    return {"sucess": True}
