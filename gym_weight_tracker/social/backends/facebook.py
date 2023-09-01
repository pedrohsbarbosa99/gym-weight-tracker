import requests
from django.conf import settings

from .oauth import BaseBackendOAuth


class FacebookAppOAuth(BaseBackendOAuth):
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

    def get_token_reponse(self, token):
        is_valid_token = self._is_valid_token(token)
        if not is_valid_token:
            return {}
        params = {"access_token": token, "fields": "email"}
        url = f"https://graph.facebook.com/v17.0/me"
        response = requests.get(url, params=params)
        return response.json()

    def get_user_details(self, response):
        return {"email": response.get("email")}
