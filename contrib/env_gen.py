"""
Django SECRET_KEY generator.
"""
from django.utils.crypto import get_random_string

chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"

CONFIG_STRING = """
DEBUG=True
SECRET_KEY=%s
ALLOWED_HOSTS=127.0.0.1, .localhost
CORS_ALLOWED_ORIGINS=http://localhost:3000
DATABASE_URL=cockroach://root@localhost:26257/defaultdb
""".strip() % get_random_string(
    50,
    chars,
)

# Writing our configuration file to '.env'
with open(".env", "w") as configfile:
    configfile.write(CONFIG_STRING)
