import json
import os
from beanie import DeleteRules
from bson import ObjectId
from pydantic import PydanticUserError
import strawberry
import razorpay
from Middleware.jwtbearer import IsAuthenticated
from models.dbschema import Orders, User, Product
from Graphql.schema.orders import (
    ResponseOrders as ror,
    InputOrders as ipor,
    InputUpdateOrders as ipuor,
)
from helper.utils import encode_input, generate_random_alphanumeric, retval
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from beanie import PydanticObjectId


# Load dotenv
load_dotenv(find_dotenv(".env"))
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
KAFKA_MAIL_TOPIC = os.getenv("KAFKA_MAIL_TOPIC")
STAGE = str(os.getenv("STAGE"))
STORE_NAME = str(os.getenv("STORE_NAME"))


async def delete_order(orderID):
    get_ord = await Orders.find_one(
        Orders.id == ObjectId(orderID),
        fetch_links=True,
    )
    await get_ord.delete(link_rule=DeleteRules.DELETE_LINKS)


async def add_order_to_db(
    encoded_data,
    info,
    razor_order_id="",
):
    try:
        # Find User
        user = None
        try:
            user = await User.get(encoded_data["userID"])
        except Exception as e:
            print(e)

        if user:
            # Find Product references
            products_ordered_ref = []
            for pid in encoded_data["productsOrdered"]:
                prod = await Product.get(pid[0])
                if prod:
                    products_ordered_ref.append(
                        {**prod.__dict__, "quantity": int(pid[1])}
                    )

            # print(products_ordered_ref)

            if products_ordered_ref:

                if encoded_data["payment_by"] == "razorpay":
                    print("Entred Razor!")

                    try:
                        new_ord = Orders(
                            **{
                                "_id": encoded_data["_id"],
                                "amount": encoded_data["amount"],
                                "user_ordered": user,
                                "userid": str(user.id),
                                "products_ordered": products_ordered_ref,
                                "razorpay_details": {
                                    "razorpay_order_id": razor_order_id
                                },
                                "payment_by": encoded_data["payment_by"],
                                "name": encoded_data["name"].title(),
                                "email": encoded_data["email"],
                                "phone_number": encoded_data["phone_number"],
                                "address": encoded_data["address"],
                                "update_address": encoded_data.get(
                                    "update_address", False
                                ),
                                "shipping_fee": encoded_data["shipping_fee"],
                                "tax": encoded_data["tax"],
                            }
                        )
                        # Inset order
                        data = await new_ord.insert()
                        return data.id
                    except Exception as e:
                        print(str(e))
                        raise e

                else:
                    print("Entred COD!")
                    try:
                        new_ord = Orders(
                            **{
                                "_id": encoded_data["_id"],
                                "amount": encoded_data["amount"],
                                "user_ordered": user,
                                "userid": str(user.id),
                                "products_ordered": products_ordered_ref,
                                "payment_by": encoded_data["payment_by"],
                                "name": encoded_data["name"].title(),
                                "email": encoded_data["email"],
                                "phone_number": encoded_data["phone_number"],
                                "address": encoded_data["address"],
                                "update_address": encoded_data.get(
                                    "update_address", False
                                ),
                                "shipping_fee": encoded_data["shipping_fee"],
                                "tax": encoded_data["tax"],
                            }
                        )

                        # Insert order
                        data = await new_ord.insert()

                        # Update inventory
                        get_ord = await Orders.get(data.id)
                        # await update_inventory(get_ord)
                        info.context["background_tasks"].add_task(
                            update_inventory, get_ord
                        )
                        info.context["background_tasks"].add_task(
                            send_order_receipt, info, get_ord
                        )

                        return data.id
                    except Exception as e:
                        print(str(e), "Error Occcured!")
                        # raise e

            else:
                return ""
        else:
            return ""
    except Exception as e:
        return ""


async def add_user_to_db(encoded_data, info):
    try:
        # Find User
        user = await User.get(encoded_data["userID"])

        if user:
            # Upadate User
            new_user = encode_input(encoded_data["userDetails"])

            if new_user["address"]["street_address"]:
                user.address.street_address = new_user["address"]["street_address"]

            if new_user["address"]["city"]:
                user.address.city = new_user["address"]["city"]

            if new_user["address"]["state"]:
                user.address.state = new_user["address"]["state"]

            if new_user["address"]["country"]:
                user.address.country = new_user["address"]["country"]

            if new_user["address"]["countryCode"]:
                user.address.countryCode = new_user["address"]["countryCode"]

            if new_user["address"]["zip_code"]:
                user.address.zip_code = new_user["address"]["zip_code"]

            if new_user["phone_number"]:
                user.phone_number = new_user["phone_number"]

            await user.save()
            print(new_user, "CURR USER")

        else:
            print(f"No user with id {encoded_data['userID']}")
    except Exception as e:
        print("Error", str(e))


def sanitize_products(products):
    # print(products)
    ans = []
    for product in products:
        tmp = {}
        tmp["quantity"] = product.quantity
        tmp["price"] = ((100 - product.discount_percent) / 100) * (product.price)
        tmp["title"] = product.title
        ans.append(tmp)

    return ans


async def update_inventory(get_ord):
    print("Update inventory")
    for product in get_ord.products_ordered:
        get_quantity = product.quantity
        get_product = await Product.get(product.id)
        if get_product:
            get_product.stock -= get_quantity
            await get_product.save()


async def send_order_receipt(info, get_ord):
    print("Sending order receipt ...")

    # Publish message to apache kafka topic to send mail
    d = datetime.strptime(str(get_ord.orderedAt), "%Y-%m-%d %H:%M:%S.%f")
    s = d.strftime("%d/%m/%Y %I:%M %p")

    producer = info.context["kafka_producer"]
    produce_data = {
        "STORE_NAME": STORE_NAME,
        "products_ordered": sanitize_products(get_ord.products_ordered),
        "tax": get_ord.tax,
        "shipping_fee": get_ord.shipping_fee,
        "order_id": str(get_ord.id),
        "orderedAt": s,
        "email": get_ord.email,
        "name": get_ord.name,
    }
    final_data = {"operation": "order_receipt", "data": produce_data}
    # print(final_data)
    await producer.send(KAFKA_MAIL_TOPIC, json.dumps(final_data).encode())


@strawberry.type
class Mutation:

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def create_order(self, data: ipor, info: strawberry.Info) -> list[str]:
        try:
            # Clean data
            # print(data.__dict__)
            encoded_data = encode_input(data.__dict__)
            # print(encoded_data)
            # Note : User will be authenticated anyway so no checks and no checks on product exists

            if encoded_data["payment_by"] == "razorpay":
                # Just create a razorpay order and send it
                client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
                razor_data = {
                    "amount": (round(encoded_data["amount"] * 0.08) * 100) + 300,
                    "currency": "INR",
                    "receipt": f"order_rcptid_{generate_random_alphanumeric(15)}",
                }
                create_order = client.order.create(data=razor_data)
                razor_order_id = create_order["id"]
                # print(create_order)

                # data = await add_order_to_db(encoded_data, razor_order_id)
                # print(data, "GOT THIS BACK")

                order_id = PydanticObjectId(oid=ObjectId())
                print(order_id)
                encoded_data["_id"] = order_id

                info.context["background_tasks"].add_task(
                    add_order_to_db, encoded_data, info, razor_order_id
                )

                if encoded_data.get("update_address", ""):
                    # Background task data base insertion of user details
                    info.context["background_tasks"].add_task(
                        add_user_to_db, encoded_data, info
                    )
                else:
                    pass
                return [razor_order_id, str(order_id)]
            else:
                # data = await add_order_to_db(encoded_data, "")

                order_id = PydanticObjectId(oid=ObjectId())
                print(order_id)
                encoded_data["_id"] = order_id

                info.context["background_tasks"].add_task(
                    add_order_to_db,
                    encoded_data,
                    info,
                    "",
                )

                if encoded_data.get("update_address", ""):
                    # Background task data base insertion of user details
                    info.context["background_tasks"].add_task(
                        add_user_to_db, encoded_data, info
                    )
                else:
                    pass

                # if data:
                #     get_ord = await Orders.get(data)
                #     await update_inventory(get_ord)
                #     # info.context["background_tasks"].add_task(update_inventory, get_ord)
                #     info.context["background_tasks"].add_task(
                #         send_order_receipt, info, get_ord
                #     )
                return ["Order Placed! Cash on delivery mode", str(order_id)]

        except Exception as e:
            return [f"Error Occured {str(e)}"]

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def update_order(self, data: ipuor, info: strawberry.Info) -> ror:
        try:
            print(data.__dict__, "Revieved data")

            original_data = data.__dict__
            encoded_data = encode_input(original_data)

            encoded_data["hasFailed"] = original_data["hasFailed"]
            encoded_data["isPending"] = original_data["isPending"]
            try:
                get_ord = await Orders.find_one(
                    Orders.id == ObjectId(encoded_data["orderID"])
                )
            except Exception as e:
                print(str(e))
                raise e
            print(encoded_data)
            del encoded_data["orderID"]
            print(get_ord, "has order")
            if get_ord:
                ord_updated = await get_ord.update({"$set": encoded_data})

                if not encoded_data["hasFailed"]:
                    # Update inventory
                    # await update_inventory(get_ord)
                    info.context["background_tasks"].add_task(update_inventory, get_ord)

                    info.context["background_tasks"].add_task(
                        send_order_receipt, info, get_ord
                    )
                return ror(data=ord_updated, err=None)
            else:
                return ror(
                    data=None, err=f"No order with orderID {encoded_data['orderID']}"
                )
        except Exception as e:
            return ror(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def delete_order(self, orderID: str, info: strawberry.Info) -> ror:
        try:
            get_ord = await Orders.find_one(
                Orders.id == ObjectId(orderID), fetch_links=True, nesting_depth=1
            )
            if get_ord:
                info.context["background_tasks"].add_task(delete_order, orderID)

                return ror(data=get_ord, err=None)
            else:
                return ror(data=None, err=f"No order with orderID {orderID}")
        except Exception as e:
            return ror(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_order_by_id(self, orderID: str) -> ror:
        try:
            get_ord = await Orders.find_one(Orders.id == ObjectId(orderID))
            if get_ord:
                return ror(data=get_ord, err=None)
            else:
                return ror(data=None, err=f"No order with orderID {orderID}")
        except Exception as e:
            return ror(data=None, err=str(e))
