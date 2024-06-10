from faker import Faker
import random
import requests
import json
import datetime
import random
import string
import os
from dotenv import find_dotenv, load_dotenv
import uuid
from genderize import Genderize


# Load dotenv
load_dotenv(find_dotenv(".env"))
RANDOMMER_KEY = os.getenv("RANDOMMER_KEY")


# User Data

# Initialize Faker generator
fake = Faker()


def get_all_cultures():
    get_cultures = requests.get(
        f"https://randommer.io/api/Name/Cultures",
        headers={"X-Api-Key": RANDOMMER_KEY},
    ).json()

    return get_cultures


get_all_cult = get_all_cultures()


def get_country_and_country_code_lookup():
    data = get_all_cult
    countries = [
        "United States",
        "Canada",
        "Germany",
        "France",
        "Italy",
        "Spain",
        "Netherlands",
        "Belgium",
        "Sweden",
        "Norway",
        "Denmark",
        "Finland",
        "Ireland",
        "United Kingdom",
        "Japan",
        "China",
        "India",
        "Brazil",
        "South Africa",
        "Russia",
    ]

    lookup = {}

    for country in countries:
        for dat in data:
            if dat["name"].lower().find(country.lower()) >= 0:
                if country not in lookup:
                    lookup[country] = dat["code"]

    lookup_phone = {
        "United States": "us",
        "Canada": "ca",
        "Germany": "de",
        "France": "fr",
        "Italy": "it",
        "Spain": "es",
        "Netherlands": "nl",
        "Belgium": "be",
        "Sweden": "sv",
        "Norway": "no",
        "Ireland": "ie",
        "Japan": "jp",
        "China": "cn",
        "Brazil": "br",
        "South Africa": "af",
        "Russia": "ru",
    }

    return lookup, lookup_phone


def get_name(nameType, quantity):
    names = requests.get(
        f"https://randommer.io/api/Name?nameType={nameType}&quantity={quantity}",
        headers={"X-Api-Key": RANDOMMER_KEY},
    ).json()
    return names


def generate_email(full_name):
    # List of famous email providers
    domains = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "aol.com",
        "protonmail.com",
    ]

    # Extracting first and last names
    first_name, last_name = full_name.split(" ")

    # Generating a unique identifier
    unique_id = str(uuid.uuid4())[:8]  # Using only the first 8 characters of the UUID

    # Creating the email name
    email_name = f"{first_name.lower()}.{last_name.lower()}_{unique_id}"

    # Ensuring the email name is 10 characters long
    # email_name = email_name[:10]

    # Appending a domain
    email_address = f"{email_name}@{random.choice(domains)}"

    return email_address


def get_email(quantity, name: str | list):
    res = []

    if isinstance(name, list):
        for i in range(quantity):
            email = generate_email(name[i])
            res.append(email)
        return res
    else:
        return generate_email(name)


def get_password(quantity):
    res = []
    for i in range(quantity):
        res.append(fake.password(length=10))

    return res


def get_dob(quantity):
    res = []
    for i in range(quantity):
        res.append(fake.date_of_birth(minimum_age=18).strftime("%Y-%m-%d"))
    return res


def get_phone_numbers(country_code, quantity):
    numbers = requests.get(
        f"https://randommer.io/api/Phone/Generate?CountryCode={country_code}&quantity={quantity}",
        headers={"X-Api-Key": RANDOMMER_KEY},
    ).json()
    print(numbers)
    return numbers


def get_random_country_code_and_country():
    currData = get_country_and_country_code_lookup()

    random_country = random.choice(list(currData[0]))
    print(random_country)

    country_code = str(currData[0][random_country])
    country_code_phone = str(currData[1][random_country])

    return [country_code, random_country, country_code_phone]


def get_address(number):

    res = []
    for i in range(number):
        tmp = get_random_country_code_and_country()

        culture = tmp[0]
        country = tmp[1]
        phone_code = tmp[-1]
        get_address = requests.get(
            f"https://randommer.io/api/Misc/Random-Address?number={1}&culture={culture}",
            headers={"X-Api-Key": RANDOMMER_KEY},
        ).json()

        for addr in get_address:
            currAddr = addr.split(",")
            tmp = {
                "street_address": currAddr[0] + "," + currAddr[1],
                "zip_code": currAddr[2],
                "city": currAddr[3],
                "state": currAddr[4],
                "country": country,
                "countryCode": culture,
                "country_code_phone": phone_code,
            }
            res.append(tmp)
    return res


def get_profile_pic_link(name):
    idx = random.randint(1, 78)
    gender = Genderize().get([name])[0]["gender"]
    if gender == "male":
        return f"https://xsgames.co/randomusers/assets/avatars/male/{idx}.jpg"
    elif gender == "female":
        return f"https://xsgames.co/randomusers/assets/avatars/female/{idx}.jpg"


TOTAL_RECORDS = 10
records = []

pics = []
for i in range(1, 5):
    if i == 1 or i == 3 or i == 5:
        pics.append(f"https://ui.shadcn.com/avatars/0{i}.png")


def get_all():
    names = get_name("fullname", TOTAL_RECORDS)
    emails = get_email(TOTAL_RECORDS, names)
    passwords = get_password(TOTAL_RECORDS)

    dobs = get_dob(TOTAL_RECORDS)
    addresses = get_address(TOTAL_RECORDS)

    final = []
    for (
        name,
        email,
        password,
        dob,
        addr,
    ) in zip(
        names,
        emails,
        passwords,
        dobs,
        addresses,
    ):
        print(addr)
        saved_code = addr["country_code_phone"]
        del addr["country_code_phone"]

        tmp = {
            "name": name,
            "email": email,
            "password": password,
            "dob": dob,
            "phone_number": get_phone_numbers(saved_code, 1)[0],
            "address": addr,
            "profile_pic": get_profile_pic_link(name),
        }
        final.append(tmp)

    with open("user.json", "w") as fp:
        json.dump(final, fp)


get_all()


# Seller Data


class Seller:
    def __init__(self):
        self.dob = (
            datetime.datetime.now()
            - datetime.timedelta(days=random.randint(365 * 20, 365 * 80))
        ).strftime("%Y-%m-%d")
        self.password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(12)
        )
        self.company_name = fake.company()
        self.seller_name = f"{fake.first_name()} {fake.last_name()}"


with open("./dataset.json", "r") as fp:
    data = json.load(fp)

for prod in data:
    get_addr = get_address(1)[0]
    saved_code = get_addr["country_code_phone"]
    del get_addr["country_code_phone"]

    seller = Seller()
    prod["seller_info"] = {
        "email": get_email(1, seller.seller_name),
        "phone_number": get_phone_numbers(saved_code, 1)[0],
        "dob": seller.dob,
        "password": seller.password,
        "company_name": seller.company_name,
        "company_address": get_addr,
        "seller_name": seller.seller_name,
        "profile_pic": get_profile_pic_link(seller.seller_name),
    }


with open("dataset.json", "w") as fp:
    json.dump(data, fp)
