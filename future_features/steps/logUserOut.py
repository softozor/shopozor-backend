from behave import given, then, when
from behave import use_fixture

from features.fixtures import *
from tests.api.utils import get_graphql_content


@given(u'un utilisateur identifié sur le Shopozor')
def step_impl(context):
    use_fixture(graphql_query, context, 'login.graphql')
    variables = {'email': context.consumer['email'], 'password': context.consumer['password']}
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)
    context.token = context.response['data']['login']['token']
    context.test.assertNotNull(context.token)


@when(u'il se déconnecte')
def step_impl(context):
    use_fixture(graphql_query, context, 'logout.graphql')
    variables = {'token': context.token}
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)


@then(u'son token d\'identification est invalidé')
def step_impl(context):
    use_fixture(failed_query_response, context)
    use_fixture(successful_logout_response, context)
    use_fixture(graphql_query, context, 'me.graphql')

    context.test.assertEqual(context.response['data'], context.successful_logout_response['data'])
    response = context.test.client.post_graphql(context.query)
    context.test.assertEqual(response['data'], context.failed_query_response['data'])
