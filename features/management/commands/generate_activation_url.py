from django.contrib.auth.tokens import default_token_generator
from django.core.management.base import BaseCommand
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from os import path
from saleor.account.models import User

# this bases on saleor.graphql.account.mutations
class Command(BaseCommand):
    help = 'Generate activation url for specified user.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User\'s e-mail')

    def handle(self, *args, **options):
        email = options['email']
        usr = User.objects.filter(email=email).first()
        uidb64 = urlsafe_base64_encode(force_bytes(usr.pk)).decode()
        print('uidb64 = ', uidb64)
        token = default_token_generator.make_token(usr)
        print('token  = ', token)
        print('url = ', 'http://www.shopozor.ch/activate/%s/%s' % (uidb64, token))