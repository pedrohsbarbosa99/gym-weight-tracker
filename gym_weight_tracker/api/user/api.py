from .schema import UserSchema
from django.core.handlers.wsgi import WSGIRequest
from ninja import Router

user_router = Router()


@user_router.get("/me", response=UserSchema)
def me(request: WSGIRequest):
    return request.user
