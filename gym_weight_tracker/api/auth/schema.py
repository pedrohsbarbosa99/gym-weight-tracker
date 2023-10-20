import warnings
from typing import Any, Callable, Dict, Optional, Type, cast

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import AbstractUser, update_last_login
from django.utils.translation import gettext_lazy as _
from ninja import ModelSchema, Schema
from ninja.errors import ValidationError
from ninja_jwt.settings import api_settings
from ninja_jwt.tokens import RefreshToken, SlidingToken, UntypedToken
from ninja_jwt.utils import token_error
from pydantic import root_validator

if api_settings.BLACKLIST_AFTER_ROTATION:
    from ninja_jwt.token_blacklist.models import BlacklistedToken

user_name_field = get_user_model().USERNAME_FIELD  # type: ignore


class AuthUserSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = [user_name_field]


class InputSchemaMixin:
    dict: Callable

    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        raise NotImplementedError("Must implement `get_response_schema`")

    def to_response_schema(self):
        _schema_type = self.get_response_schema()
        return _schema_type(**self.dict())


class TokenInputSchemaMixin(InputSchemaMixin):
    _user: Optional[AbstractUser] = None

    _default_error_messages = {
        "no_active_account": _(
            "No active account found with the given credentials"
        )
    }

    def check_user_authentication_rule(self) -> None:
        if not api_settings.USER_AUTHENTICATION_RULE(self._user):
            raise ValidationError(
                self._default_error_messages["no_active_account"]
            )

    @classmethod
    def validate_values(cls, values: Dict) -> dict:
        if user_name_field not in values and "password" not in values:
            raise ValidationError(
                {
                    user_name_field: f"{user_name_field} is required",
                    "password": "password is required",
                }
            )

        if not values.get(user_name_field):
            raise ValidationError(
                {user_name_field: f"{user_name_field} is required"}
            )

        if not values.get("password"):
            raise ValidationError({"password": "password is required"})

        _user = authenticate(**values)
        cls._user = _user

        if not (_user is not None and _user.is_active):
            raise ValidationError(
                cls._default_error_messages["no_active_account"]
            )

        return values

    def output_schema(self) -> Schema:
        warnings.warn(
            "output_schema() is deprecated in favor of "
            "to_response_schema()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.to_response_schema()

    @classmethod
    def get_token(cls, user: AbstractUser) -> Dict:
        raise NotImplementedError(
            "Must implement `get_token` method for `TokenObtainSerializer` subclasses"
        )


class TokenObtainInputSchemaBase(ModelSchema, TokenInputSchemaMixin):
    class Config:
        model = get_user_model()
        model_fields = ["password", user_name_field]

    @root_validator(pre=True)
    def validate_inputs(cls, values: Dict) -> dict:
        return cls.validate_values(values)

    @root_validator
    def post_validate(cls, values: Dict) -> dict:
        return cls.post_validate_schema(values)

    @classmethod
    def post_validate_schema(cls, values: Dict) -> dict:
        """
        This is a post validate process which is common for any token generating schema.
        :param values:
        :return:
        """
        # get_token can return values that wants to apply to `OutputSchema`

        data = cls.get_token(cls._user)

        if not isinstance(data, dict):
            raise Exception("`get_token` must return a `typing.Dict` type.")

        values.update(data)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, cls._user)

        return values

    def to_response_schema(self):
        _schema_type = self.get_response_schema()
        return _schema_type(**self.dict(exclude={"password"}))


class TokenObtainPairOutputSchema(AuthUserSchema):
    refresh: str
    access: str


class TokenObtainPairInputSchema(TokenObtainInputSchemaBase):
    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return TokenObtainPairOutputSchema

    @classmethod
    def get_token(cls, user: AbstractUser) -> Dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        refresh = cast(RefreshToken, refresh)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        return values


class TokenObtainSlidingOutputSchema(AuthUserSchema):
    token: str


class TokenObtainSlidingInputSchema(TokenObtainInputSchemaBase):
    @classmethod
    def get_response_schema(cls) -> Type:
        return TokenObtainSlidingOutputSchema

    @classmethod
    def get_token(cls, user: AbstractUser) -> Dict:
        values = {}
        slide_token = SlidingToken.for_user(user)
        values["token"] = str(slide_token)
        return values


class TokenRefreshInputSchema(Schema, InputSchemaMixin):
    refresh: str

    @root_validator
    def validate_schema(cls, values: Dict) -> dict:
        if not values.get("refresh"):
            raise ValidationError({"refresh": "token is required"})
        return values

    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return TokenRefreshOutputSchema


class TokenRefreshOutputSchema(Schema):
    refresh: str
    access: Optional[str]

    @root_validator
    @token_error
    def validate_schema(cls, values: Dict) -> dict:
        if not values.get("refresh"):
            raise ValidationError({"refresh": "refresh token is required"})

        refresh = RefreshToken(values["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)
        values.update(data)
        return values


class TokenRefreshSlidingInputSchema(Schema, InputSchemaMixin):
    token: str

    @root_validator
    def validate_schema(cls, values: Dict) -> dict:
        if not values.get("token"):
            raise ValidationError({"token": "token is required"})
        return values

    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return TokenRefreshSlidingOutputSchema


class TokenRefreshSlidingOutputSchema(Schema):
    token: str

    @root_validator
    @token_error
    def validate_schema(cls, values: Dict) -> dict:
        if not values.get("token"):
            raise ValidationError({"token": "token is required"})

        token = SlidingToken(values["token"])

        # Check that the timestamp in the "refresh_exp" claim has not
        # passed
        token.check_exp(api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        # Update the "exp" and "iat" claims
        token.set_exp()
        token.set_iat()
        values.update({"token": str(token)})
        return values


class TokenVerifyInputSchema(Schema, InputSchemaMixin):
    token: str

    @root_validator
    @token_error
    def validate_schema(cls, values: Dict) -> dict:
        if not values.get("token"):
            raise ValidationError({"token": "token is required"})
        token = UntypedToken(values["token"])

        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "ninja_jwt.token_blacklist" in settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")

        return values

    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return Schema

    def to_response_schema(self):
        return {}


class TokenBlacklistInputSchema(Schema, InputSchemaMixin):
    refresh: str

    @root_validator
    @token_error
    def validate_schema(cls, values: Dict) -> dict:
        if not values.get("refresh"):
            raise ValidationError({"refresh": "refresh token is required"})
        refresh = RefreshToken(values["refresh"])
        try:
            refresh.blacklist()
        except AttributeError:
            pass
        return values

    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return Schema

    def to_response_schema(self):
        return {}


__deprecated__ = {
    "TokenBlacklistSerializer": TokenBlacklistInputSchema,
    "TokenVerifySerializer": TokenVerifyInputSchema,
    "TokenRefreshSlidingSerializer": TokenRefreshSlidingOutputSchema,
    "TokenRefreshSlidingSchema": TokenRefreshSlidingInputSchema,
    "TokenRefreshSerializer": TokenRefreshOutputSchema,
    "TokenRefreshSchema": TokenRefreshInputSchema,
    "TokenObtainSlidingOutput": TokenObtainSlidingOutputSchema,
    "TokenObtainSerializer": TokenObtainInputSchemaBase,
    "TokenObtainPairOutput": TokenObtainPairOutputSchema,
    "TokenObtainPairSerializer": TokenObtainPairInputSchema,
    "TokenObtainSlidingSerializer": TokenObtainSlidingInputSchema,
}


def __getattr__(name: str) -> Any:  # pragma: no cover
    if name in __deprecated__:
        value = __deprecated__[name]
        warnings.warn(
            f"'{name}' is deprecated. Use '{value.__name__}' instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return value
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
