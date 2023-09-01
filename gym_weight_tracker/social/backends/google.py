import requests
from django.conf import settings
from django.contrib.auth import get_user_model

from .oauth import BaseBackendOAuth

User = get_user_model()


class Google(BaseBackendOAuth):
    def _token_info(self, **params):
        return requests.get(
            f"{settings.OAUTH2_GOOGLE_URL}/tokeninfo",
            params=params,
        )

    def get_token_reponse(self, token):
        response = self._token_info(id_token=token)
        if response.status_code == 200:
            return response.json()
        response = self._token_info(access_token=token)
        if response.status_code == 200:
            return response.json()
        return {}

    def get_user_details(self, response):
        return {"email": response.get("email")}
