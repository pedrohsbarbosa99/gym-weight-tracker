from typing import List
from gym_weight_tracker.account.models import User
from gym_weight_tracker.api.schema import (
    ExerciseSchema,
    UserSchema,
    ProgressionSchema,
    ProgressionInputSchema,
    ExerciseInputSchema,
)
from gym_weight_tracker.core.models import Exercise, Progression
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404
from django.db.models import F

from .controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(title="Light Weight Baby", auth=JWTAuth())
api.register_controllers(NinjaJWTDefaultController)


@api.get("/me", response=UserSchema, tags=["user"])
def me(request: WSGIRequest):
    return request.user


@api.get("/exercises", response=List[ExerciseSchema], tags=["exercise"])
def exercises(request: WSGIRequest):
    return Exercise.objects.all()


@api.patch("/exercises/{exercise_id}", tags=["exercise"])
def update_exercise(request, exercise_id: int, payload: ExerciseInputSchema):
    Exercise.objects.filter(pk=exercise_id).update(**payload.dict(exclude_none=True))
    return {"Success": True}


@api.post("/exercises", response=ExerciseSchema, tags=["exercise"])
def create_exercise(request, payload: ExerciseInputSchema):
    return Exercise.objects.create(**payload.dict())


@api.delete("/exercises", response=ExerciseSchema, tags=["exercise"])
def delete_exercise(request, tasks_id: int):
    exercise = get_object_or_404(Exercise, id=tasks_id)
    exercise.delete()
    return {"sucess": True}


@api.get(
    "/exercises/{exercise_id}/progressions",
    response=List[ProgressionSchema],
    tags=["progression"],
)
def progressions(request: WSGIRequest, exercise_id: int):
    return Progression.objects.annotate(exercise_name=F("exercise__name")).filter(
        exercise_id=exercise_id,
    )


@api.post("/progressions", response=ProgressionSchema, tags=["progression"])
def progression_create(request: WSGIRequest, payload: ProgressionInputSchema):
    user = get_object_or_404(User, id=request.user.id)
    exercise = get_object_or_404(Exercise, id=payload.exercise_id)

    progression = Progression(user=user, exercise=exercise, weight=payload.weight)
    progression.save()

    return progression
