import strawberry


@strawberry.type
class Query:
    @strawberry.field
    async def hello() -> str:
        return "hello"
