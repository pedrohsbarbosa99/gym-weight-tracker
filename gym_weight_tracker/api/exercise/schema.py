from ninja import Schema
from ninja.errors import HttpError
from pydantic import validator

from gym_weight_tracker.core.models import Exercise


class ExerciseSchema(Schema):
    id: int
    name: str
    description: str = ""
    difficulty_level: str


class ExerciseInputSchema(Schema):
    name: str = None
    description: str = None
    difficulty_level: str = None

    @validator("name")
    def validate_name(cls, v):
        if Exercise.objects.filter(name=v).exists():
            raise HttpError(400, "Este nome já está sendo usado.")
        return v
