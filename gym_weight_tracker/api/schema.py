from ninja import Schema
from datetime import date
from gym_weight_tracker.core.models import Exercise
from ninja.errors import HttpError

from pydantic import validator


class ExerciseSchema(Schema):
    name: str


class ExerciseInputSchema(Schema):
    name: str

    @validator("name")
    def validate_name(cls, v):
        if Exercise.objects.filter(name=v).exists():
            raise HttpError(400, "Este nome já está sendo usado.")
        return v


class ProgressionInputSchema(Schema):
    exercise_id: int
    weight: int


class ProgressionSchema(Schema):
    id: int = None
    exercise_name: str = None
    weight: int
    created_at: date = None


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None
    first_name: str = None
    last_name: str = None
