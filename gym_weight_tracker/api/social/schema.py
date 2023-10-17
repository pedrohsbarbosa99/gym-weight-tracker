from enum import Enum
from typing import Dict, cast

from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema
from ninja_jwt.tokens import RefreshToken

from .utils import import_social_validator

User = get_user_model()
user_name_field = User.USERNAME_FIELD  # type: ignore


class AuthUserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = [user_name_field]


class Plataform(str, Enum):
    google = "google"
    facebook = "facebook"


class TokenSocialInput(Schema):
    token: str


class ConvertTokenSchema(Schema):
    @classmethod
    def output_schema(cls, plataform, user_token: TokenSocialInput) -> Dict:
        social_backend = cls.get_validator(plataform)
        user = social_backend.authenticate(user_token.token)
        values = {}
        refresh = RefreshToken.for_user(user)
        refresh = cast(RefreshToken, refresh)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        values["email"] = user.email
        return values

    @classmethod
    def get_validator(self, plataform):
        return import_social_validator(plataform)


class TokenSchema(AuthUserSchema):
    refresh: str
    access: str
