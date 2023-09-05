from ninja import Schema
from ninja.router import Router
from ninja_jwt.schema import (
    TokenObtainPairInputSchema,
    TokenObtainPairOutputSchema,
    TokenRefreshInputSchema,
    TokenRefreshOutputSchema,
    TokenVerifyInputSchema,
)

auth_router = Router()


@auth_router.post(
    "/pair", response=TokenObtainPairOutputSchema, url_name="token_obtain_pair"
)
def obtain_token(request, user_token: TokenObtainPairInputSchema):
    return user_token.output_schema()


@auth_router.post(
    "/refresh",
    response=TokenRefreshOutputSchema,
    url_name="token_refresh",
    auth=None,
)
def refresh_token(request, refresh_token: TokenRefreshInputSchema):
    return refresh_token.to_response_schema()


@auth_router.post(
    "/verify",
    response={200: Schema},
    url_name="token_verify",
)
def verify_token(request, token: TokenVerifyInputSchema):
    return token.to_response_schema()
