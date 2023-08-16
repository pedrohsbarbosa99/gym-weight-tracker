from datetime import datetime

from django.shortcuts import get_object_or_404
from ninja import Schema
from pydantic import validator

from gym_weight_tracker.core.models import Exercise


class ProgressionInputSchema(Schema):
    exercise_id: int
    weight: int

    @validator("exercise_id")
    def validate_exercise_id(cls, v):
        get_object_or_404(Exercise, id=v)
        return v


class ProgressionSchema(Schema):
    id: int = None
    exercise_name: str = None
    weight: int
    created_at: datetime = None


class LastProgressionSchema(Schema):
    exercise_id: int
    exercise_name: str
    last_weight: int = None
    old_last_weight: int = None
    last_date: datetime = None
