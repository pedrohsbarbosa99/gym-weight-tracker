from ninja import Schema


class UserSchema(Schema):
    username: str
    email: str = None
    first_name: str = None
    last_name: str = None
