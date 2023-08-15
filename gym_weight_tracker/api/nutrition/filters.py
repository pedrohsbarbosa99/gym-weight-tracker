from typing import Optional

from ninja import Field, FilterSchema


class FoodFilterSchema(FilterSchema):
    name__icontains: Optional[str]
    category__name__icontains: Optional[str]
    search: Optional[str] = Field(q=["name__icontains", "category__name__icontains"])
