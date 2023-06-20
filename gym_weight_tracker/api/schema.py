from ninja import Schema
from ninja import ModelSchema
from datetime import date
from gym_weight_tracker.core.models import Exercise
from ninja.errors import HttpError


class ExerciseSchema(ModelSchema):
    class Config:
        model = Exercise
        model_fields = "__all__"

    def validate_name(self, value: str):
        if Exercise.objects.filter(name=value).exists():
            raise HttpError(400, "Este nome já está sendo usado.")


class ExerciseInputSchema(ModelSchema):
    class Config:
        model = Exercise
        model_fields = ["name"]


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
