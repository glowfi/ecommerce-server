import strawberry


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def hello() -> str:
        return "hello"
