from typing import Optional
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from ninja import Field, FilterSchema
from django.db.models import Q


class ExerciseFilterSchema(FilterSchema):
    search: Optional[str] = Field(q=[])

    def filter(self, queryset: QuerySet) -> QuerySet:
        if self.search:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity("name", self.search)
            )
            return queryset.filter(
                Q(name__unaccent__icontains=self.search)
                | Q(similarity__gte=0.5),
            ).order_by("-similarity")
        return queryset.filter(self.get_filter_expression())
