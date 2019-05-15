import os.path

from behave import fixture
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from features.utils import *
from saleor.account.models import User
from shopozor.permissions import add_permissions


@fixture
def graphql_query(context, queryfile):
    context.query = get_query_from_file(queryfile)
    yield context.query
    # the query is deleted in the after_scenario hook
    # because a scenario might involve many queries
    # if we delete the query from the context now,
    # then the scenario cleanup will throw an error
    # as it will need to delete context.query several times


@fixture
def permissions(context):
    add_permissions(User, Permission, ContentType)


@fixture
def unknown(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'NewConsumer.json'))
    context.unknown = user_data
    yield user_data
    del context.unknown


@fixture
def consumer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Consommateur.json'))
    create_database_user(user_data)
    context.consumer = user_data
    yield user_data
    del context.consumer


@fixture
def inactive_customer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'InactiveConsumer.json'))
    create_database_user(user_data)
    context.inactive_customer = user_data
    yield user_data
    del context.inactive_customer


@fixture
def producer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Producteur.json'))
    create_database_user(user_data)
    context.producer = user_data
    yield user_data
    del context.producer


@fixture
def manager(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Responsable.json'))
    create_database_user(user_data)
    context.manager = user_data
    yield context.manager
    del context.manager


@fixture
def rex(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Rex.json'))
    create_database_user(user_data)
    context.rex = user_data
    yield user_data
    del context.rex


@fixture
def softozor(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Softozor.json'))
    create_database_superuser(user_data)
    context.softozor = user_data
    yield user_data
    del context.softozor


@fixture
def wrong_credentials_response(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Responses', 'WrongCredentials.json'))
    context.wrong_credentials_response = data
    yield data
    del context.wrong_credentials_response


@fixture
def user_not_admin_response(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Responses', 'Consommateur.json'))
    context.user_not_admin_response = data
    yield data
    del context.user_not_admin_response


@fixture
def failed_query_response(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Logout', 'Responses', 'QueryResponseAfterLogout.json'))
    context.failed_query_response = data
    yield context.failed_query_response
    del context.failed_query_response


@fixture
def successful_logout_response(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Logout', 'Responses', 'Success.json'))
    context.successful_logout_response = data
    yield context.successful_logout_response
    del context.successful_logout_response


@fixture
def successful_signup(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'RegisterConsumer', 'Responses', 'SuccessfulConsumerCreation.json'))
    context.successful_signup = data
    yield context.successful_signup
    del context.successful_signup


@fixture
def expired_account_confirmation_link(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'RegisterConsumer', 'Responses', 'ExpiredAccountConfirmationLink.json'))
    context.expired_account_confirmation_link = data
    yield context.expired_account_confirmation_link
    del context.expired_account_confirmation_link


@fixture
def successful_account_confirmation(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'RegisterConsumer', 'Responses', 'SuccessfulAccountConfirmation.json'))
    context.successful_account_confirmation = data
    yield context.successful_account_confirmation
    del context.successful_account_confirmation


@fixture
def password_not_compliant_response(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'RegisterConsumer', 'Responses', 'NonCompliantPassword.json'))
    context.password_not_compliant_response = data
    yield context.password_not_compliant_response
    del context.password_not_compliant_response
