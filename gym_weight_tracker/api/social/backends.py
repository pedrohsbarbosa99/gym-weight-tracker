import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


def validate_google_token(token):
    response = requests.get(
        f"{settings.OAUTH2_GOOGLE_URL}/tokeninfo?id_token={token}"
    )
    if response.status_code == 200:
        if email := response.json().get("email"):
            user = User.objects.filter(email=email).first()
            return user or AnonymousUser()
    response = requests.get(
        f"{settings.OAUTH2_GOOGLE_URL}/tokeninfo?access_token={token}"
    )
    if response.status_code == 200:
        if email := response.json().get("email"):
            user = User.objects.filter(email=email).first()
            return user or AnonymousUser()
    return AnonymousUser()


validators = {
    "google": validate_google_token,
}
