from tests.api.conftest import ApiClient
from django.contrib.auth.models import AnonymousUser
from behave import use_fixture
from features.fixtures import *


def before_feature(context, feature):
    login_or_signin = ['login', 'signup']
    # check if feature.tags contains any elements of login_or_signin
    if any(tag in feature.tags for tag in login_or_signin):
        use_fixture(unknown, context)

    if 'login' in feature.tags:
        use_fixture(wrong_credentials_response, context)
        use_fixture(user_not_admin_response, context)

    if 'signup' in feature.tags:
        use_fixture(successful_signup, context)
        use_fixture(expired_account_confirmation_link, context)
        use_fixture(successful_account_confirmation, context)
        use_fixture(password_not_compliant_response, context)


def before_scenario(context, scenario):
    if 'user-accounts' in scenario.tags:
        # the following fixtures add data to the database
        # therefore they need to be added before each scenario
        # because the database is cleaned up after each scenario
        use_fixture(permissions, context)
        use_fixture(consumer, context)
        use_fixture(producer, context)
        use_fixture(manager, context)
        use_fixture(rex, context)
        use_fixture(softozor, context)
        use_fixture(inactive_customer, context)


def after_scenario(context, scenario):
    if hasattr(context, 'query'):
        del context.query


def django_ready(context):
    context.test.client = ApiClient(user=AnonymousUser())
    context.django = True
