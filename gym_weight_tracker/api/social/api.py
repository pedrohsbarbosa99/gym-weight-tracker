from django.core.handlers.wsgi import WSGIRequest
from ninja.router import Router
from ninja_jwt.tokens import RefreshToken

from .schema import ConvertTokenSchema, Plataform, TokenSchema
from .utils import import_social_validator

social_router = Router()


@social_router.post(  # TODO change detail message on plataform error
    "convert-token/{plataform}",
    response=TokenSchema,
    auth=None,
)
def convert_token(
    request: WSGIRequest,
    plataform: Plataform,
    payload: ConvertTokenSchema,
):
    validator = import_social_validator(plataform)
    user = validator.validate(payload.token)

    refresh = RefreshToken.for_user(user)

    return {
        "email": user.email,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
