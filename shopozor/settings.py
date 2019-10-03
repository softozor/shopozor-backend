from datetime import timedelta
from saleor.settings import *

import os

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware',
                       'django.middleware.common.CommonMiddleware']
    MIDDLEWARE = CORS_MIDDLEWARE + MIDDLEWARE
    INSTALLED_APPS.append('corsheaders')

INSTALLED_APPS.remove('saleor.graphql')
INSTALLED_APPS.append('shopozor')

ROOT_URLCONF = 'shopozor.urls'

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=360),
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256'
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'shopozor.password_validation.SpecialCharacterValidator',
    },
    {
        'NAME': 'shopozor.password_validation.NumberAndLetterValidator',
    }
]

TEST_RUNNER = "unit_tests.runner.PytestTestRunner"

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

DEFAULT_COUNTRY = os.environ.get("DEFAULT_COUNTRY", "CH")
DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "CHF")

WSGI_APPLICATION = "shopozor.wsgi.application"

# TODO: this only holds for e2e, not for production!
# TODO: the EMAIL_HOST needs to come from the environment variables as it will be different on the jelastic infrastructure as in the docker-compose
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
