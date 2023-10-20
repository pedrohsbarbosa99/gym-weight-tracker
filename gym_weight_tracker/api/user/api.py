from django.core.handlers.wsgi import WSGIRequest
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from .schema import UserSchema

user_router = Router(auth=JWTAuth())


@user_router.get("/me", response=UserSchema)
def me(request: WSGIRequest):
    return request.user
