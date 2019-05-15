import graphene

from saleor.graphql.account.schema import AccountMutations, AccountQueries
# from saleor.graphql.checkout.schema import CheckoutMutations, CheckoutQueries
from saleor.graphql.core.schema import CoreMutations
# from saleor.graphql.discount.schema import DiscountMutations, DiscountQueries
# from saleor.graphql.menu.schema import MenuMutations, MenuQueries
# from saleor.graphql.order.schema import OrderMutations, OrderQueries
# from saleor.graphql.page.schema import PageMutations, PageQueries
# from saleor.graphql.payment.schema import PaymentMutations, PaymentQueries
# from saleor.graphql.product.schema import ProductMutations, ProductQueries
# from saleor.graphql.shipping.schema import ShippingMutations, ShippingQueries
# from saleor.graphql.shop.schema import ShopMutations, ShopQueries

from shopozor.graphql.auth.schema import AuthMutations

class Query(AccountQueries):
    node = graphene.Node.Field()


class Mutations(AuthMutations, AccountMutations):
    pass


schema = graphene.Schema(Query, Mutations)
