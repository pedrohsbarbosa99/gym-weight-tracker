from ninja import FilterSchema, Field
from typing import Optional


class FoodFilterSchema(FilterSchema):
    name__icontains: Optional[str]
    category__name__icontains: Optional[str]
    search: Optional[str] = Field(q=["name__icontains", "category__name__icontains"])
