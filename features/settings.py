from shopozor.settings import *
from datetime import timedelta
import json
from os import environ
import os.path

FIXTURES_FOLDER = os.path.join('features', 'fixtures')
GRAPHQL_QUERIES_FOLDER = os.path.join('features', 'graphql')

INSTALLED_APPS.append('behave_django')
INSTALLED_APPS.append('features')

ACCEPTANCE_TESTING = True

# TODO: really necessary???
if DEBUG:
    ALLOWED_HOSTS.append('testserver')

JWT_EXPIRATION_DELTA_IN_DAYS = environ.get('JWT_EXPIRATION_DELTA_IN_DAYS')
JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS = environ.get(
    'JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS')
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = environ.get('JWT_ALGORITHM')

if JWT_EXPIRATION_DELTA_IN_DAYS is None or JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS is None or JWT_SECRET_KEY is None or JWT_ALGORITHM is None:
    raise Exception('Graphql JWT parameters not defined.')

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=int(JWT_EXPIRATION_DELTA_IN_DAYS)),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=int(JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS)),
    'JWT_SECRET_KEY': JWT_SECRET_KEY,
    'JWT_ALGORITHM': JWT_ALGORITHM
}
