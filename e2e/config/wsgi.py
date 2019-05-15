from django.core.wsgi import get_wsgi_application
import json
import os
import sys

activationScriptFilename = os.path.join(
    'PATH_TO_VIRTUAL_ENV_PLACEHOLDER', 'bin', 'activate_this.py')
try:
    # the PATH_TO_VIRTUAL_ENV variable is defined by our jps
    exec(open(activationScriptFilename).read())
except IOError:
    sys.stderr.write("Couldn't read file: ", activationScriptFilename)

os.environ['SECRET_KEY'] = 'SECRET_KEY_PLACEHOLDER'
os.environ['ALLOWED_HOSTS'] = 'ALLOWED_HOSTS_PLACEHOLDER'
os.environ['DATABASE_URL'] = 'DATABASE_URL_PLACEHOLDER'
os.environ['CACHE_URL'] = 'CACHE_URL_PLACEHOLDER'
os.environ['JWT_EXPIRATION_DELTA_IN_DAYS'] = 'JWT_EXPIRATION_DELTA_IN_DAYS_PLACEHOLDER'
os.environ['JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS'] = 'JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS_PLACEHOLDER'
os.environ['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY_PLACEHOLDER'
os.environ['JWT_ALGORITHM'] = 'JWT_ALGORITHM_PLACEHOLDER'

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'DJANGO_SETTINGS_MODULE_PLACEHOLDER')

application = get_wsgi_application()
