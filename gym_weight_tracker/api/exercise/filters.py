from typing import Optional
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from ninja import FilterSchema


class ExerciseFilterSchema(FilterSchema):
    search: Optional[str]

    def filter(self, queryset: QuerySet) -> QuerySet:
        if self.search:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity("name", self.search)
            )
            return queryset.filter(
                self.get_filter_expression(),
                similarity__gte=0.6,
            ).order_by("-similarity")
        return queryset.filter(self.get_filter_expression())
