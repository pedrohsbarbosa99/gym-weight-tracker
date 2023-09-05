from django.core.handlers.wsgi import WSGIRequest
from ninja.router import Router

from .schema import (
    ConvertTokenSchema,
    Plataform,
    TokenSchema,
    TokenSocialInput,
)

social_router = Router()


@social_router.post(  # TODO change detail message on plataform error
    "convert-token/{plataform}",
    response=TokenSchema,
    auth=None,
)
def convert_token(
    request: WSGIRequest,
    plataform: Plataform,
    user_token: TokenSocialInput,
):
    return ConvertTokenSchema.output_schema(plataform, user_token)
