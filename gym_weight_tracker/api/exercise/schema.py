from gym_weight_tracker.core.models import Exercise
from ninja.errors import HttpError
from ninja import Schema
from pydantic import validator


class ExerciseSchema(Schema):
    id: int
    name: str


class ExerciseInputSchema(Schema):
    name: str

    @validator("name")
    def validate_name(cls, v):
        if Exercise.objects.filter(name=v).exists():
            raise HttpError(400, "Este nome já está sendo usado.")
        return v
