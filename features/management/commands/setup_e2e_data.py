from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from features.utils import *
from saleor.account.models import User
from shopozor.permissions import add_permissions


def create_permissions():
    add_permissions(User, Permission, ContentType)


def create_users():
    for persona in 'Consommateur', 'Producteur', 'Responsable', 'Rex':
        user_data = get_data_from_json_fixture(os.path.join(
            'Authentication', 'Credentials', persona + '.json'))
        create_database_user(user_data)


def create_superusers():
    user_data = get_data_from_json_fixture(os.path.join(
        'Authentication', 'Credentials', 'Softozor.json'))
    create_database_superuser(user_data)


class Command(BaseCommand):
    help = 'Fills up the database with the relevant data for end-to-end testing.'

    def handle(self, *args, **options):
        create_permissions()
        create_users()
        create_superusers()
