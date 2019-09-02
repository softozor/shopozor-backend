from behave import given, then, when
from features.utils.graphql.loader import get_query_from_file
from shopozor.models import Shop
from tests.api.utils import get_graphql_content

import features.types


def query_shops(client):
    query = get_query_from_file('shops.graphql')
    response = client.post_graphql(query)
    return get_graphql_content(response)


def query_shop_catalogue(client, shop_id, category_id):
    query = get_query_from_file('shopCatalogue.graphql')
    variables = {
        'shopId': shop_id,
        'categoryId': category_id
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


@given(u'le Shop le plus proche de chez lui')
def step_impl(context):
    # TODO: define Incognito's GPS coordinates
    # TODO: get the closest shop to those coords
    context.shop_id = 1


@when(u'Incognito demande quels Shops il peut visiter')
def step_impl(context):
    test_client = context.test.client
    context.response = query_shops(test_client)


@when(u'Incognito en visite le stand {category_id:ProductCategoryType}')
def step_impl(context, category_id):
    context.category_id = category_id
    test_client = context.test.client
    context.response = query_shop_catalogue(
        test_client, context.shop_id, context.category_id)


@then(u'il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale')
def step_impl(context):
    context.test.assertEqual(context.expected_shop_list, context.response)

# TODO: check that the shop catalogue fixture is not empty
@then(u'il obtient la liste de tous les Produits qui y sont publiés')
def step_impl(context):
    context.test.assertEqual(
        context.expected_shop_catalogues[context.shop_id][context.category_id], context.response)

    # Lorsqu'Incognito y inspecte un Produit
    # Alors il en obtient la description détaillée
