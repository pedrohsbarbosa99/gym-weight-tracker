from ninja import Schema


class ConvertTokenSchema(Schema):
    token: str


class TokenSchema(Schema):
    email: str
    refresh: str
    access: str
