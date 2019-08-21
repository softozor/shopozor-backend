from faker import Faker
from features.faker.providers.geo import Provider as ShopozorGeoProvider
from features.faker.providers.product import Provider as ProductProvider

import os
import unidecode


class FakeDataFactory:

    categories = (
        'Fruits & Légumes', 'Viandes', 'Fromages', 'Epicerie', 'Crèmerie', 'Boulangerie', 'Boissons', 'Traiteur', 'Maison & Jardin'
    )

    def __init__(self, max_nb_products_per_producer=10, max_nb_producers_per_shop=10):
        self.__fake = Faker('fr_CH')
        self.__fake.seed('features')
        self.__fake.add_provider(ShopozorGeoProvider)
        self.__fake.add_provider(ProductProvider)
        self.__MAX_NB_PRODUCERS_PER_SHOP = max_nb_producers_per_shop
        self.__MAX_NB_PRODUCTS_PER_PRODUCER = max_nb_products_per_producer

    def create_email(self, first_name, last_name):
        domain_name = self.__fake.free_email_domain()
        return unidecode.unidecode('%s.%s@%s' % (first_name, last_name, domain_name))

    def create_consumers(self, start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            result.append({
                'id': start_index + id,
                'email': self.__fake.email(),
                'isActive': True,
                'isStaff': False,
                'isSuperUser': False,
                'permissions': []
            })
        return result

    def create_producers(self, start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            first_name = self.__fake.first_name()
            last_name = self.__fake.last_name()
            result.append({
                'id': start_index + id,
                # get rid of any potential French accent from the first and last name
                'email': self.create_email(first_name, last_name),
                'isActive': True,
                'isStaff': True,
                'isSuperUser': False,
                'first_name': first_name,
                'last_name': last_name,
                'permissions': []
            })
        return result

    def create_managers(self, start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            first_name = self.__fake.first_name()
            last_name = self.__fake.last_name()
            result.append({
                'id': start_index + id,
                # get rid of any potential French accent from the first and last name
                'email': self.create_email(first_name, last_name),
                'isActive': True,
                'isStaff': True,
                'isSuperUser': False,
                'first_name': first_name,
                'last_name': last_name,
                'permissions': [{
                    'code': 'MANAGE_PRODUCERS'
                }]
            })
        return result

    def create_rex(self, start_index):
        return {
            'id': start_index,
            'email': 'rex@%s' % self.__fake.free_email_domain(),
            'isActive': True,
            'isStaff': True,
            'isSuperUser': False,
            'permissions': [
                {
                    'code': 'MANAGE_STAFF'
                },
                {
                    'code': 'MANAGE_USERS'
                },
                {
                    'code': 'MANAGE_PRODUCERS'
                },
                {
                    'code': 'MANAGE_MANAGERS'
                }
            ]
        }

    def create_softozor(self, start_index):
        return {
            'id': start_index,
            'email': 'softozor@%s' % self.__fake.free_email_domain(),
            'isActive': True,
            'isStaff': True,
            'isSuperUser': True,
            'permissions': []
        }

    def __staff(self, pk, user_id):
        return {
            'fields': {
                'user_id': user_id
            },
            'model': 'shopozor.staff',
            'pk': pk
        }

    def create_staff(self, producers):
        offset = producers[0]['id']
        return [self.__staff(user['id'] - offset + 1, user['id']) for user in producers]

    def __try_to_get_random_elements(self, elements, length):
        try:
            return self.__fake.random_elements(
                elements=elements, length=length, unique=True)
        except ValueError:
            return []

    def __productstaff(self, pk, product_id, producer_id):
        return {
            'fields': {
                'product_id': product_id,
                'staff_id': producer_id
            },
            'model': 'shopozor.productstaff',
            'pk': pk
        }

    def create_productstaff(self, producers, products):
        product_ids = [product['pk'] for product in products]
        result = []
        productstaff_pk = 1
        for producer in producers:
            nb_products = self.__fake.random.randint(
                0, self.__MAX_NB_PRODUCTS_PER_PRODUCER)
            producer_product_ids = self.__try_to_get_random_elements(
                product_ids, nb_products)
            for producer_product_id in producer_product_ids:
                result.append(self.__productstaff(
                    productstaff_pk, producer_product_id, producer['id']))
                productstaff_pk += 1
            product_ids = [
                id for id in product_ids if id not in producer_product_ids]
        return result

    def __shop(self, pk, variant_ids):
        latitude = float(self.__fake.local_latitude())
        longitude = float(self.__fake.local_longitude())
        return self.__fake.shop(pk, latitude, longitude, variant_ids)

    def create_shops(self, producers, productstaff, product_variants, list_size=1):
        result = []

        producer_ids = [producer['id'] for producer in producers]

        for shop_id in range(0, list_size):
            nb_producers = self.__fake.random.randint(
                0, self.__MAX_NB_PRODUCERS_PER_SHOP)
            shop_producer_ids = self.__try_to_get_random_elements(
                producer_ids, nb_producers)
            shop_product_ids = [item['fields']['product_id'] for item in productstaff if item['model']
                                == 'shopozor.productstaff' and item['fields']['staff_id'] in shop_producer_ids]
            variant_ids = [variant['pk']
                           for variant in product_variants if variant['fields']['product'] in shop_product_ids]
            producer_ids = [
                id for id in producer_ids if id not in shop_producer_ids]
            result.append(self.__shop(shop_id + 1, variant_ids))

        return result

    def __category(self, pk, name):
        return {
            'fields': {
                # TODO: generate random image
                'background_image': 'category-backgrounds/accessories.jpg',
                'background_image_alt': '',
                'description': '',
                'description_json': {
                    'blocks': [{
                        'data': {},
                        'depth': 0,
                        'entityRanges': [],
                        'inlineStyleRanges': [],
                        'key': '',
                        'text': '',
                        'type': 'unstyled'
                    }],
                    'entityMap': {}
                },
                'level': 0,
                'lft': 1,
                'name': name,
                'parent': None,
                'rght': 2,
                'seo_description': '',
                'seo_title': '',
                'slug': self.__fake.slug(),
                'tree_id': pk
            },
            'model': 'product.category',
            'pk': pk
        }

    def create_categories(self):
        result = []
        pk = 1
        for category in self.categories:
            result.append(self.__category(pk, category))
        return result

    def __producttype(self, pk):
        return {
            'fields': {
                # TODO: does this field mean that the corresponding products have no variants? --> an empty variant seems to be assigned to such products, probably in order to be able to define attributes on the variant
                'has_variants': self.__fake.has_variants(),
                'is_shipping_required': False,
                'meta': {
                    'taxes': {
                        'vatlayer': {
                            'code': 'standard',
                            'description': ''
                        }
                    }
                },
                'name': self.__fake.producttype_name(),
                'weight': self.__fake.weight()
            },
            'model': 'product.producttype',
            'pk': pk
        }

    # TODO: for each category, there will be producttypes?
    def create_producttypes(self, list_size=1):
        result = []
        for pk in range(1, list_size + 1):
            result.append(self.__producttype(pk))
        return result

    # TODO: for each category and related producttype, generate product?

    # TODO: be careful with product generation; if the product belongs to a producttype with has_variants == False, then it needs to have an empty variant
    # TODO: for each category and producttype, generate products?
    # def __product(self, pk, categories, producttypes):
    #     return {
    #         'fields': {
    #         'attributes': "{\"15\": \"46\", \"21\": \"68\"}",
    #         'category': 8,
    #         'charge_taxes': true,
    #         'description': 'Find your sea legs and then lose the power to use them with extra strong seaman\u2019s lager. Don\u2019t drink and sail, me hearties!',
    #         'description_json': {
    #             'blocks': [
    #             {
    #                 'data': {},
    #                 'depth': 0,
    #                 'entityRanges': [],
    #                 'inlineStyleRanges': [],
    #                 'key': '',
    #                 'text': 'Find your sea legs and then lose the power to use them with extra strong seaman\u2019s lager. Don\u2019t drink and sail, me hearties!',
    #                 'type': 'unstyled'
    #             }
    #             ],
    #             'entityMap': {}
    #         },
    #         'is_published': true,
    #         'meta': {
    #             'taxes': {
    #             'vatlayer': {
    #                 'code': 'standard',
    #                 'description': ''
    #             }
    #             }
    #         },
    #         'name': 'Seaman Lager',
    #         'price': {
    #             '_type': 'Money',
    #             'amount': '3.00',
    #             'currency': 'CHF'
    #         },
    #         'product_type': 11,
    #         'publication_date': null,
    #         'seo_description': 'Find your sea legs and then lose the power to use them with extra strong seaman\u2019s lager. Don\u2019t drink and sail, me hearties!',
    #         'seo_title': '',
    #         'updated_at': '2019-03-06T12:47:38.530Z',
    #         'weight': 1.0
    #         },
    #         'model': 'product.product',
    #         'pk': 83
    #     }
