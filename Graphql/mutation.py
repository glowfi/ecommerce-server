import strawberry
from Graphql.Mutate.seller import Mutation as sellerMutation
from Graphql.Mutate.product import Mutation as productMutation
from Graphql.Mutate.category import Mutation as categoryMutation
from Graphql.Mutate.user import Mutation as userMutation
from Graphql.Mutate.orders import Mutation as ordersMutation
from Graphql.Mutate.reviews import Mutation as reviewsMutation
from Graphql.Mutate.wishlist import Mutation as wishlistMutation
from Graphql.Mutate.admin import Mutation as adminMutation
from Graphql.Mutate.auth import Mutation as authMutation


@strawberry.type
class Mutation(
    sellerMutation,
    productMutation,
    categoryMutation,
    userMutation,
    ordersMutation,
    reviewsMutation,
    wishlistMutation,
    authMutation,
    adminMutation,
):
    @strawberry.mutation
    async def hello() -> str:
        return "hello"
