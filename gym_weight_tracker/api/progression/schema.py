from datetime import datetime

from ninja import Schema


class ProgressionInputSchema(Schema):
    exercise_id: int
    weight: int


class ProgressionSchema(Schema):
    id: int = None
    exercise_name: str = None
    weight: int
    created_at: datetime = None


class LastProgressionSchema(Schema):
    name: str
    exercise_id: int
    last_weight: int = None
    old_last_weight: int = None
    last_date: datetime = None
