from django.contrib.auth import get_user_model
from ninja.errors import HttpError

User = get_user_model()


class BaseBackendOAuth:
    def get_token_reponse(self, token):
        raise NotImplementedError("`get_token_reponse()` must be implemented.")

    def get_user_details(self, response):
        raise NotImplementedError("`get_user_details()` must be implemented.")

    def validate(self, token):
        response = self.get_token_reponse(token)
        user_info = self.get_user_details(response)
        if email := user_info.get("email"):
            if user := User.objects.filter(email=email).first():
                return user
        raise HttpError(400, "Token Invalido")
