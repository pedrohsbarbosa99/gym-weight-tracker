from django.conf import settings
from django.utils.module_loading import import_string


def import_social_validator(validator_string):
    validator = import_string(settings.SOCIAL_VALIDATORS[validator_string])
    return validator()
