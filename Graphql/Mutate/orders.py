import json
import os
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


# Load dotenv
load_dotenv(find_dotenv(".env"))
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
KAFKA_MAIL_TOPIC = os.getenv("KAFKA_MAIL_TOPIC")
STAGE = str(os.getenv("STAGE"))
STORE_NAME = str(os.getenv("STORE_NAME"))


def stripper(data):
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = stripper(v)
        if v not in ("", None, {}):
            new_data[k] = v
    return new_data


async def add_order_to_db(encoded_data, razor_order_id=""):
    try:
        # Find User
        user = await User.get(encoded_data["userID"], fetch_links=True)
        # print(user)

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
                    new_ord = Orders(
                        **{
                            "amount": encoded_data["amount"],
                            "user_ordered": user,
                            "userid": str(user.id),
                            "products_ordered": products_ordered_ref,
                            "razorpay_details": {"razorpay_order_id": razor_order_id},
                            "payment_by": encoded_data["payment_by"],
                            "name": encoded_data["name"].title(),
                            "email": encoded_data["email"],
                            "phone_number": encoded_data["phone_number"],
                            "address": encoded_data["address"],
                            "update_address": encoded_data["update_address"],
                            "shipping_fee": encoded_data["shipping_fee"],
                            "tax": encoded_data["tax"],
                        }
                    )
                else:
                    new_ord = Orders(
                        **{
                            "amount": encoded_data["amount"],
                            "user_ordered": user,
                            "userid": str(user.id),
                            "products_ordered": products_ordered_ref,
                            "payment_by": encoded_data["payment_by"],
                            "name": encoded_data["name"].title(),
                            "email": encoded_data["email"],
                            "phone_number": encoded_data["phone_number"],
                            "address": encoded_data["address"],
                            "update_address": encoded_data["update_address"],
                            "shipping_fee": encoded_data["shipping_fee"],
                            "tax": encoded_data["tax"],
                        }
                    )

                # Inset order
                data = await new_ord.insert()
                return data.id
            else:
                return ""
        else:
            return ""
    except Exception as e:
        return ""


async def add_user_to_db(encoded_data, info):
    try:
        # Find User
        user = await User.get(encoded_data["userID"], fetch_links=True)

        if user:
            # Upadate User
            new_user = stripper(encoded_data["userDetails"])

            new_user_address = new_user["address"]

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

        else:
            print(f"No user with id {encoded_data['userID']}")
    except Exception as e:
        print("Error", str(e))


def sanitize_products(products):
    ans = []
    for product in products:
        tmp = {}
        tmp["quantity"] = product.quantity
        tmp["price"] = product.price
        tmp["title"] = product.title
        ans.append(tmp)

    return ans


async def send_order_receipt(info, get_ord):

    # Publish message to apache kafka topic to send mail
    d = datetime.strptime(str(get_ord.orderedAt), "%Y-%m-%d %H:%M:%S.%f")
    s = d.strftime("%m/%d/%Y %I:%M %p")

    producer = info.context["kafka_producer"]
    produce_data = {
        "STORE_NAME": STORE_NAME,
        "products_ordered": sanitize_products(get_ord.products_ordered),
        "tax": get_ord.tax,
        "shipping_fee": get_ord.shipping_fee,
        "order_id": get_ord.id,
        "orderedAt": s,
        "email": get_ord.email,
        "name": get_ord.name,
    }
    final_data = {"operation": "order_receipt", "data": produce_data}
    print(final_data)
    await producer.send(KAFKA_MAIL_TOPIC, json.dumps(final_data).encode())


@strawberry.type
class Mutation:

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def create_order(self, data: ipor, info: strawberry.Info) -> list[str]:
        try:
            # Clean data
            encoded_data = encode_input(data.__dict__)
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

                data = await add_order_to_db(encoded_data, razor_order_id)

                if encoded_data["update_address"]:
                    # Background task data base insertion of user details
                    info.context["background_tasks"].add_task(
                        add_user_to_db, encoded_data, info
                    )
                else:
                    pass
                return [razor_order_id, data]
            else:
                data = await add_order_to_db(encoded_data, "")

                if encoded_data["update_address"]:
                    # Background task data base insertion of user details
                    info.context["background_tasks"].add_task(
                        add_user_to_db, encoded_data, info
                    )
                else:
                    pass

                if data:
                    get_ord = await Orders.get(data)
                    info.context["background_tasks"].add_task(
                        send_order_receipt, info, get_ord
                    )
                return ["Order Placed! Cash on delivery mode"]

        except Exception as e:
            return [f"Error Occured {str(e)}"]

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def update_order(self, data: ipuor, info: strawberry.Info) -> ror:
        try:
            encoded_data = encode_input(data.__dict__)
            get_ord = await Orders.get(encoded_data["orderID"])
            del encoded_data["orderID"]
            if get_ord:
                ord_updated = await get_ord.update({"$set": encoded_data})

                # Update inventory
                for product in get_ord.products_ordered:
                    get_quantity = product.quantity
                    get_product = await Product.get(product.id)
                    if get_product:
                        get_product.stock -= get_quantity
                        await get_product.save()

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

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_order_by_id(self, orderID: str) -> ror:
        try:
            get_ord = await Orders.get(orderID)
            if get_ord:
                return ror(data=get_ord, err=None)
            else:
                return ror(data=None, err=f"No order with orderID {orderID}")
        except Exception as e:
            return ror(data=None, err=str(e))
