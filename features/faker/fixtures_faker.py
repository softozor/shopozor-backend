from django.conf import settings
from faker import Faker
from features.faker.providers.geo import Provider as ShopozorGeoProvider
from features.faker.providers.product import Provider as ProductProvider
from features.faker.providers.time import Provider as DateTimeProvider

import dateutil.parser
import itertools
import os
import unidecode


class FakeDataFactory:

    category_types = {
        'Fruits': ('Fruit'),
        'Légumes': ('Légume'),
        'Boucherie': ('Boucherie'),
        'Epicerie': ('Epicerie'),
        'Laiterie': ('Laiterie'),
        'Boulangerie': ('Boulangerie'),
        'Boissons': ('Boisson'),
        'Traiteur': ('Traiteur'),
        'Nettoyages': ('Nettoyage'),
        'Soins corporels': ('Soin corporel'),
        'Objets pour la maison': ('Objet pour la maison')
    }

    def __init__(self, max_nb_products_per_producer=10, max_nb_producers_per_shop=10, max_nb_variants_per_product=10, max_nb_images_per_product=10):
        self.__fake = Faker('fr_CH')
        self.__fake.seed('features')
        self.__fake.add_provider(ShopozorGeoProvider)
        self.__fake.add_provider(ProductProvider)
        self.__fake.add_provider(DateTimeProvider)
        self.__MAX_NB_PRODUCERS_PER_SHOP = max_nb_producers_per_shop
        self.__MAX_NB_PRODUCTS_PER_PRODUCER = max_nb_products_per_producer
        self.__MAX_NB_IMAGES_PER_PRODUCT = max_nb_images_per_product
        self.__MAX_NB_VARIANTS_PER_PRODUCT = max_nb_variants_per_product

    def create_email(self, first_name, last_name):
        domain_name = self.__fake.free_email_domain()
        # get rid of any potential French accent from the first and last name
        return unidecode.unidecode('%s.%s@%s' % (first_name, last_name, domain_name)).lower()

    def __create_consumer(self, id):
        return {
            'id': id,
            'email': self.__fake.email(),
            'isActive': True,
            'isStaff': False,
            'isSuperUser': False,
            'permissions': []
        }

    def create_consumers(self, start_index, list_size=1):
        return [self.__create_consumer(start_index + id) for id in range(0, list_size)]

    def __address(self):
        return {
            'streetAddress': self.__fake.street_address(),
            'city': self.__fake.city(),
            'postalCode': self.__fake.postcode(),
            'country': 'CH'
        }

    def __create_producer(self, id):
        first_name = self.__fake.first_name()
        last_name = self.__fake.last_name()
        return {
            'id': id,
            'email': self.create_email(first_name, last_name),
            'isActive': True,
            'isStaff': True,
            'isSuperUser': False,
            'firstName': first_name,
            'lastName': last_name,
            'permissions': [],
            'address': self.__address()
        }

    def create_producers(self, start_index, list_size=1):
        return [self.__create_producer(start_index + id) for id in range(0, list_size)]

    def __create_manager(self, id):
        first_name = self.__fake.first_name()
        last_name = self.__fake.last_name()
        return {
            'id': id,
            'email': self.create_email(first_name, last_name),
            'isActive': True,
            'isStaff': True,
            'isSuperUser': False,
            'firstName': first_name,
            'lastName': last_name,
            'permissions': [{
                'code': 'MANAGE_PRODUCERS'
            }],
            'address': self.__address()
        }

    def create_managers(self, start_index, list_size=1):
        return [self.__create_manager(start_index + id) for id in range(0, list_size)]

    def __create_rex(self, id):
        first_name = self.__fake.first_name()
        last_name = self.__fake.last_name()
        return {
            'id': id,
            'email': self.create_email(first_name, last_name),
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
            ],
            'address': self.__address()
        }

    def create_reges(self, start_index, list_size=1):
        return [self.__create_rex(start_index + id) for id in range(0, list_size)]

    def create_softozor(self, id):
        first_name = self.__fake.first_name()
        last_name = self.__fake.last_name()
        return {
            'id': id,
            'email': self.create_email(first_name, last_name),
            'isActive': True,
            'isStaff': True,
            'isSuperUser': True,
            'permissions': []
        }

    def create_softozors(self, start_index, list_size=1):
        return [self.create_softozor(start_index + id) for id in range(0, list_size)]

    def __staff(self, pk, user_id):
        return {
            'fields': {
                'user_id': user_id,
                'description': self.__fake.description()
            },
            'model': 'shopozor.staff',
            'pk': pk
        }

    def create_staff(self, producers):
        offset = producers[0]['id']
        return [self.__staff(user['id'] - offset + 1, user['id']) for user in producers]

    def __get_random_elements(self, elements, length):
        return self.__fake.random_elements(
            elements=elements, length=length, unique=True)

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
        total_nb_products = 0
        for producer in producers:
            nb_products = self.__fake.random.randint(
                1, self.__MAX_NB_PRODUCTS_PER_PRODUCER)
            producer_product_ids = self.__get_random_elements(
                product_ids, nb_products)
            for producer_product_id in producer_product_ids:
                result.append(self.__productstaff(
                    productstaff_pk, producer_product_id, producer['id']))
                productstaff_pk += 1
            product_ids = [
                id for id in product_ids if id not in producer_product_ids]
            total_nb_products += nb_products
        print('#products assigned to producers: %d out of %d' %
              (total_nb_products, len(products)))
        return result

    def __shop(self, pk, variant_ids):
        latitude = float(self.__fake.local_latitude())
        longitude = float(self.__fake.local_longitude())
        return self.__fake.shop(pk, latitude, longitude, variant_ids)

    def create_shops(self, producers, productstaff, product_variants, list_size=1):
        result = []

        producer_ids = [producer['id'] for producer in producers]

        total_nb_producers = 0
        for shop_id in range(0, list_size):
            nb_producers = self.__fake.random.randint(
                1, self.__MAX_NB_PRODUCERS_PER_SHOP)
            shop_producer_ids = self.__get_random_elements(
                producer_ids, nb_producers)
            shop_product_ids = [item['fields']['product_id'] for item in productstaff if item['model']
                                == 'shopozor.productstaff' and item['fields']['staff_id'] in shop_producer_ids]
            variant_ids = [variant['pk']
                           for variant in product_variants if variant['fields']['product'] in shop_product_ids]
            producer_ids = [
                id for id in producer_ids if id not in shop_producer_ids]
            result.append(self.__shop(shop_id + 1, variant_ids))
            total_nb_producers += nb_producers
        print('#producers assigned to shops: %d out of %d' %
              (total_nb_producers, len(producers)))
        return result

    def __category(self, pk, name):
        return {
            'fields': {
                'background_image': self.__fake.category_image_url(),
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
        start_pk = 1
        return [self.__category(pk, category) for pk, category in enumerate(self.category_types, start_pk)]

    def __producttype(self, pk, name):
        return {
            'fields': {
                # we currently simplify this has_variant thing and put it to True all the time
                # if a product belongs to a producttype with has_variants == False, then it needs to have an empty variant
                # only the product and productvariant attributes carry information in such a case, which might be useful
                # but not now
                'has_variants': True,
                'is_shipping_required': False,
                'name': name,
                'weight': self.__fake.weight()
            },
            'model': 'product.producttype',
            'pk': pk
        }

    def create_producttypes(self):
        producttypes = list(itertools.chain.from_iterable(
            self.category_types.values()))
        start_pk = 1
        return [self.__producttype(pk, type) for pk, type in enumerate(producttypes, start_pk)]

    def __product(self, pk, category_id, producttype_id):
        description = self.__fake.description()
        return {
            'fields': {
                'category': category_id,
                'charge_taxes': True,
                'description': description,
                'description_json': {
                    'blocks': [
                        {
                            'data': {},
                            'depth': 0,
                            'entityRanges': [],
                            'inlineStyleRanges': [],
                            'key': '',
                            'text': description,
                            'type': 'unstyled'
                        }
                    ],
                    'entityMap': {}
                },
                'is_published': self.__fake.is_published(),
                'name': self.__fake.product_name(),
                'price': self.__fake.money_amount(max_amount=0),
                'product_type': producttype_id,
                'publication_date': self.__fake.publication_date(),
                'seo_description': description,
                'seo_title': '',
                'weight': self.__fake.weight()
            },
            'model': 'product.product',
            'pk': pk
        }

    def create_products(self, categories, producttypes, list_size=1):
        result = []
        nb_published_products = 0
        for pk in range(1, list_size + 1):
            category_name = self.__fake.random_element(
                elements=self.category_types.keys())
            category_id = [category['pk']
                           for category in categories if category['fields']['name'] == category_name][0]
            producttype_name = self.__fake.random_element(
                elements=self.category_types[category_name])
            producttype_id = [
                type['pk'] for type in producttypes if type['fields']['name'] == producttype_name][0]
            product = self.__product(pk, category_id, producttype_id)
            result.append(product)
            nb_published_products += int(product['fields']['is_published'])
        print('#published products: %d out of %d' %
              (nb_published_products, len(result)))
        return result

    def __shopozor_product(self, pk, product_id, publication_date):
        return {
            'fields': {
                'product_id': product_id,
                'conservation_mode': self.__fake.conservation_mode(),
                'conservation_until': self.__fake.conservation_until(start_date=publication_date),
                'vat_rate': self.__fake.vat_rate()
            },
            'model': 'shopozor.product',
            'pk': pk
        }

    def create_shopozor_products(self, products):
        start_pk = 1
        return [self.__shopozor_product(pk, product['pk'], dateutil.parser.parse(product['fields']['publication_date'])) for pk, product in enumerate(products, start_pk)]

    def __productvariant(self, pk, product):
        quantity = self.__fake.quantity()
        cost_price = self.__fake.variant_cost_price()
        return {
            'fields': {
                'attributes': '{}',
                'cost_price': cost_price,
                'name': self.__fake.variant_name(),
                # TODO: this value is not really faked; it should not be part of the faker provider
                'price_override': self.__fake.price_override(cost_price),
                'product': product['pk'],
                'quantity': quantity,
                'quantity_allocated': self.__fake.quantity_allocated(quantity),
                'sku': self.__fake.sku(),
                'track_inventory': True,
                'weight': self.__fake.weight()
            },
            'model': 'product.productvariant',
            'pk': pk
        }

    def create_productvariants(self, products):
        result = []
        pk = 1
        for product in products:
            # any product has at least one variant
            nb_variants = self.__fake.random.randint(
                1, self.__MAX_NB_VARIANTS_PER_PRODUCT)
            for _ in range(0, nb_variants):
                result.append(self.__productvariant(pk, product))
                pk += 1
        return result

    def __productimage(self, pk, product_id):
        return {
            'model': 'product.productimage',
            'pk': pk,
            'fields': {
                'sort_order': 0,
                'product': product_id,
                'image': self.__fake.product_image_url(),
                'ppoi': '0.5x0.5',
                'alt': ''
            }
        }

    def create_productimages(self, product_ids):
        result = []
        pk = 1
        for product_id in product_ids:
            nb_imgs = self.__fake.random.randint(
                0, self.__MAX_NB_IMAGES_PER_PRODUCT)
            for _ in range(0, nb_imgs):
                result.append(self.__productimage(pk, product_id))
                pk += 1
        return result

    def __vat(self, pk):
        return {
            'model': 'django_prices_vatlayer.vat',
            'pk': pk,
            'fields': {
                'country_code': 'CH',
                'data': '{"country_name":"Switzerland","standard_rate":%f,"reduced_rates":{"reduced":%f,"special":%f}}'
                % (settings.VAT_SERVICES * 100, settings.VAT_PRODUCTS * 100, settings.VAT_SPECIAL * 100)
            }
        }

    def __ratetypes(self, pk):
        return {
            'model': 'django_prices_vatlayer.ratetypes',
            'pk': pk,
            'fields': {
                'types': '["reduced","special"]'
            }
        }

    def create_vat_layer(self):
        return [self.__vat(1), self.__ratetypes(1)]

    def __margindefinition(self, pk, role, margin):
        return {
            'model': 'shopozor.margindefinitions',
            'pk': pk,
            'fields': {
                'role': role,
                'margin': margin
            }
        }

    def create_margindefns(self):
        return [
            self.__margindefinition(
                1, 'manager', settings.MANAGER_MARGIN * 100),
            self.__margindefinition(2, 'rex', settings.REX_MARGIN * 100),
            self.__margindefinition(
                3, 'softozor', settings.SOFTOZOR_MARGIN * 100)
        ]
