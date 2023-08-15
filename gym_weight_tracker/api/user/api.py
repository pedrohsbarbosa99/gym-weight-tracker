from django.core.handlers.wsgi import WSGIRequest
from ninja import Router

from .schema import UserSchema

user_router = Router()


@user_router.get("/me", response=UserSchema)
def me(request: WSGIRequest):
    return request.user
