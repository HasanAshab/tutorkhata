from .base import *
from .base import env, BASE_DIR


DEBUG = False

ALLOWED_HOSTS = ["tutorkhata.pythonanywhere.com"]

# CACHE NOT REQUIRED FOR NOW
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
#         "LOCATION": "127.0.0.1:11211",
#     }
# }

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = True


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("DB_HOST"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": env("DB_SSLMODE"),
        }
    },
}
