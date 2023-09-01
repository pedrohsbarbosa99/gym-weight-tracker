from ninja import Schema
from enum import Enum


class ConvertTokenSchema(Schema):
    token: str


class TokenSchema(Schema):
    email: str
    refresh: str
    access: str


class Plataform(str, Enum):
    google = "google"
    facebook = "facebook"
