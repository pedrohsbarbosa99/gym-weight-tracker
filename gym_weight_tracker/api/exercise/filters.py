from ninja import FilterSchema, Field
from typing import Optional


class ExerciseFilterSchema(FilterSchema):
    name__icontains: Optional[str]
    search: Optional[str] = Field(q=["name__icontains"])
