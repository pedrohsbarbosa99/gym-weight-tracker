from django.apps import AppConfig
from django.db.models import CharField

from .lookups import Similarity


class CoreConfig(AppConfig):
    CharField.register_lookup(Similarity)
    name = "gym_weight_tracker.core"
