from ninja import Schema
from ninja_extra import ControllerBase, api_controller, http_post
from ninja_extra.permissions import AllowAny
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings

schema = SchemaControl(api_settings)


class TokenVerificationController(ControllerBase):
    auto_import = False

    @http_post(
        "/verify",
        response={200: Schema},
        url_name="token_verify",
    )
    def verify_token(self, token: schema.verify_schema):
        return token.to_response_schema()


class TokenObtainPairController(ControllerBase):
    auto_import = False

    @http_post(
        "/pair",
        response=schema.obtain_pair_schema.get_response_schema(),
        url_name="token_obtain_pair",
        auth=None,
    )
    def obtain_token(self, user_token: schema.obtain_pair_schema):
        user_token.check_user_authentication_rule()
        return user_token.to_response_schema()

    @http_post(
        "/refresh",
        response=schema.obtain_pair_refresh_schema.get_response_schema(),
        url_name="token_refresh",
        auth=None,
    )
    def refresh_token(self, refresh_token: schema.obtain_pair_refresh_schema):
        return refresh_token.to_response_schema()


@api_controller("/token", permissions=[AllowAny], tags=["token"])
class NinjaJWTDefaultController(TokenVerificationController, TokenObtainPairController):
    """NinjaJWT Default controller for obtaining and refreshing tokens"""

    auto_import = False
