from django.conf import settings
from django.utils.module_loading import import_string


def import_social_validator(vlidator_string):
    validator = import_string(settings.SOCIAL_VALIDATORS[vlidator_string])
    return validator()
