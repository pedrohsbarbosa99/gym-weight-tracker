from abc import ABC, abstractmethod

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.errors import HttpError

User = get_user_model()


class Backend(ABC):
    @abstractmethod
    def validate(self):
        raise NotImplementedError()


class Google(Backend):
    def _get_token_info(self, **params):
        return requests.get(
            f"{settings.OAUTH2_GOOGLE_URL}/tokeninfo",
            params=params,
        )

    def _get_user_info(self, token):
        response = self._get_token_info(id_token=token)
        if response.status_code == 200:
            return response.json()
        response = self._get_token_info(access_token=token)
        if response.status_code == 200:
            return response.json()
        raise HttpError(400, "Token Invalido")

    def validate(self, token):
        user_info = self._get_user_info(token)
        if email := user_info.get("email"):
            if user := User.objects.filter(email=email).first():
                return user
        raise HttpError(400, "Token Invalido")
