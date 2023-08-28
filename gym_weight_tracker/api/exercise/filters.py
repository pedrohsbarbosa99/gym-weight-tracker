from typing import Optional
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from ninja import Field, FilterSchema


class ExerciseFilterSchema(FilterSchema):
    search: Optional[str] = Field(q=["name__unaccent__trigram_similar"])

    def filter(self, queryset: QuerySet) -> QuerySet:
        queryset = queryset.annotate(similarity=TrigramSimilarity("name", self.search))
        return queryset.filter(self.get_filter_expression(), similarity__gt=0.5)
