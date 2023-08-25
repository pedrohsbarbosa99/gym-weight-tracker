from typing import Optional

from ninja import Field, FilterSchema


class ExerciseFilterSchema(FilterSchema):
    name__icontains: Optional[str]
    search: Optional[str] = Field(q=["name__icontains"])
