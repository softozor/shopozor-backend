import jwt
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Decode JWT.'

    def add_arguments(self, parser):
        parser.add_argument('token', type=str, help='Token to decode')
        parser.add_argument('-s', '--secret', type=str, help='Decoding secret')
        parser.add_argument('-a', '--algorithm', type=str, help='Decoding algorithm')

    def handle(self, *args, **options):
        token = options['token']
        secret = options['secret'] if options['secret'] else settings.GRAPHQL_JWT['JWT_SECRET_KEY']
        algorithm = options['algorithm'] if options['algorithm'] else settings.GRAPHQL_JWT['JWT_ALGORITHM']
        decoded = jwt.decode(token, key=secret, algorithm=algorithm)
        print('decoded = ', decoded)
