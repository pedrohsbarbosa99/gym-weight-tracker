from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from ninja.errors import HttpError
from ninja.router import Router
from ninja_jwt.tokens import RefreshToken

from .backends import validators
from .schema import ConvertTokenSchema, TokenSchema

social_router = Router()


@social_router.post(
    "convert-token/{source}",
    response=TokenSchema,
    auth=None,
)
def convert_token(
    request: WSGIRequest,
    source: str,
    payload: ConvertTokenSchema,
):
    if validator := validators.get(source):
        user = validator(payload.token)
    else:
        raise HttpError(400, "Source invalido")

    if isinstance(user, AnonymousUser):
        raise HttpError(400, "Token Invalido")
    refresh = RefreshToken.for_user(user)

    return {
        "email": user.email,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
