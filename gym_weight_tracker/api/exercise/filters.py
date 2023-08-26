from typing import Optional

from ninja import Field, FilterSchema


class ExerciseFilterSchema(FilterSchema):
    name__unaccent__similarity: Optional[str]
    search: Optional[str] = Field(q=["name__unaccent__similarity"])
