from abc import ABC, abstractmethod

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.errors import HttpError

User = get_user_model()


class Backend(ABC):
    @abstractmethod
    def validate(self, token):
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
        return {}

    def validate(self, token):
        user_info = self._get_user_info(token)
        if email := user_info.get("email"):
            if user := User.objects.filter(email=email).first():
                return user
        raise HttpError(400, "Token Invalido")


class FaceBook(Backend):
    app_id = settings.FACEBOOK_APP_ID
    app_secret = settings.FACEBOOK_APP_SECRET

    def _is_valid_token(self, token):
        params = {
            "input_token": token,
            "access_token": f"{self.app_id}|{self.app_secret}",
        }
        response = requests.get(
            f"https://graph.facebook.com/debug_token",
            params=params,
        )
        if response.status_code == 200:
            return response.json()["data"]["is_valid"]
        return False

    def _get_user_info(self, token):
        is_valid_token = self._is_valid_token(token)
        if not is_valid_token:
            return {}
        params = {"access_token": token, "fields": "email"}
        url = f"https://graph.facebook.com/v17.0/me"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return {}

    def validate(self, token):
        user_info = self._get_user_info(token)
        if email := user_info.get("email"):
            if user := User.objects.filter(email=email).first():
                return user
        raise HttpError(400, "Token Invalido")
