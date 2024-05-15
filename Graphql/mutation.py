import strawberry
from Graphql.Mutate.seller import Mutation as sellerMutation
from Graphql.Mutate.product import Mutation as productMutation
from Graphql.Mutate.category import Mutation as categoryMutation


@strawberry.type
class Mutation(sellerMutation, productMutation, categoryMutation):
    @strawberry.mutation
    async def hello() -> str:
        return "hello"
