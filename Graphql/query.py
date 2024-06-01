import strawberry
from Graphql.Query.seller import Query as sellerQuery
from Graphql.Query.product import Query as productQuery
from Graphql.Query.category import Query as categoryQuery
from Graphql.Query.user import Query as userQuery
from Graphql.Query.wishlist import Query as wishlistQuery
from Graphql.Query.orders import Query as ordersQuery
from Graphql.Query.reviews import Query as reviewsQuery
from Graphql.Query.otp import Query as otpQuery
from Graphql.Query.confirmaccount import Query as confirmaccountQuery


@strawberry.type
class Query(
    sellerQuery,
    productQuery,
    categoryQuery,
    userQuery,
    wishlistQuery,
    ordersQuery,
    reviewsQuery,
    otpQuery,
    confirmaccountQuery,
):
    @strawberry.field
    async def hello() -> str:
        return "hello"
