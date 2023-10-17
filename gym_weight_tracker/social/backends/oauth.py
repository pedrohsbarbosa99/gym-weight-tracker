from django.contrib.auth import get_user_model
from ninja.errors import HttpError

User = get_user_model()


class BaseBackendOAuth:
    def get_token_reponse(self, token):
        raise NotImplementedError("`get_token_reponse()` must be implemented.")

    def get_user_details(self, response):
        raise NotImplementedError("`get_user_details()` must be implemented.")

    def authenticate(self, token):
        response = self.get_token_reponse(token)
        user_info = self.get_user_details(response)
        if username := user_info.get(User.USERNAME_FIELD):
            filters = {User.USERNAME_FIELD: username}
            if user := User.objects.filter(**filters).first():
                return user
        raise HttpError(400, "Token Invalido")
