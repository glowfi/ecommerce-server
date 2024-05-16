import strawberry
from Graphql.Mutate.seller import Mutation as sellerMutation
from Graphql.Mutate.product import Mutation as productMutation
from Graphql.Mutate.category import Mutation as categoryMutation
from Graphql.Mutate.user import Mutation as userMutation
from Graphql.Mutate.orders import Mutation as userOrders
from Graphql.Mutate.reviews import Mutation as userReviews
from Graphql.Mutate.wishlist import Mutation as userWishlist


@strawberry.type
class Mutation(
    sellerMutation,
    productMutation,
    categoryMutation,
    userMutation,
    userOrders,
    userReviews,
    userWishlist,
):
    @strawberry.mutation
    async def hello() -> str:
        return "hello"
