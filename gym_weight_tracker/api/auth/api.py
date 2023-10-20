from ninja import Schema
from ninja.router import Router
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings

auth_router = Router()

schema = SchemaControl(api_settings)


@auth_router.post(
    "/pair",
    response=schema.obtain_pair_schema.get_response_schema(),
    url_name="token_obtain_pair",
)
def obtain_token(request, user_token: schema.obtain_pair_schema):
    user_token.check_user_authentication_rule()
    return user_token.output_schema()


@auth_router.post(
    "/refresh",
    response=schema.obtain_pair_refresh_schema.get_response_schema(),
    url_name="token_refresh",
    auth=None,
)
def refresh_token(request, refresh_token: schema.obtain_pair_refresh_schema):
    return refresh_token.to_response_schema()


@auth_router.post(
    "/verify",
    response={200: Schema},
    url_name="token_verify",
)
def verify_token(request, token: schema.verify_schema):
    return token.to_response_schema()
