from .schema import ExerciseInputSchema, ExerciseSchema
from typing import List
from django.core.handlers.wsgi import WSGIRequest
from gym_weight_tracker.core.models import Exercise
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

exercise_router = Router()


@exercise_router.get("", response=List[ExerciseSchema])
@paginate
def exercises(request: WSGIRequest):
    return Exercise.objects.all()


@exercise_router.patch("/{exercise_id}")
def update_exercise(request, exercise_id: int, payload: ExerciseInputSchema):
    Exercise.objects.filter(pk=exercise_id).update(**payload.dict(exclude_none=True))
    return {"Success": True}


@exercise_router.post("", response=ExerciseSchema)
def create_exercise(request, payload: ExerciseInputSchema):
    return Exercise.objects.create(**payload.dict())


@exercise_router.delete("/{exercise_id}", response=ExerciseSchema)
def delete_exercise(request, exercise_id: int):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    exercise.delete()
    return {"sucess": True}
