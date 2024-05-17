import strawberry
from models.dbschema import Orders, User, Product
from Graphql.schema.orders import (
    ResponseOrders as ror,
    InputOrders as ipor,
    # InputUpdateOrders as ipuor,
)
from helper.utils import encode_input


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_order(self, data: ipor) -> ror:
        try:
            encoded_data = encode_input(data.__dict__)
            # Find User
            user = await User.get(encoded_data["userID"], fetch_links=True)
            if user:
                # Find product
                prod = await Product.get(encoded_data["productID"], fetch_links=True)
                if prod:
                    new_ord = Orders(
                        **{
                            "user_ordered": user,
                            "product_ordered": prod,
                        }
                    )
                    ord_ins = await new_ord.insert()
                    return ror(data=ord_ins, err=None)
                else:
                    return ror(
                        data=None,
                        err=f"No product found with id {encoded_data['productID']}",
                    )
            else:
                return ror(
                    data=None, err=f"No user found with id {encoded_data['userID']}"
                )

        except Exception as e:
            return ror(data=None, err=str(e))

    # @strawberry.mutation
    # async def update_order(self, data: ipuor, orderID: str) -> ror:
    #     try:
    #         encoded_data = encode_input(data.__dict__)
    #         get_ord = await Orders.get(orderID)
    #         if get_ord:
    #             ord_updated = await get_ord.update({"$set": encoded_data})
    #             return ror(data=ord_updated, err=None)
    #         else:
    #             return ror(data=None, err=f"No order with orderID {orderID}")
    #     except Exception as e:
    #         return ror(data=None, err=str(e))

    @strawberry.mutation
    async def delete_order(self, orderID: str) -> ror:
        try:
            get_ord = await Orders.get(orderID)
            if get_ord:
                ord_deleted = await get_ord.delete()
                return ror(data=ord_deleted, err=None)
            else:
                return ror(data=None, err=f"No order with orderID {orderID}")
        except Exception as e:
            return ror(data=None, err=str(e))

    @strawberry.mutation
    async def get_order_by_id(self, orderID: str) -> ror:
        try:
            get_ord = await Orders.get(orderID)
            if get_ord:
                return ror(data=get_ord, err=None)
            else:
                return ror(data=None, err=f"No order with orderID {orderID}")
        except Exception as e:
            return ror(data=None, err=str(e))
