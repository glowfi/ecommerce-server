> Ecommerce server

### Technologies used:

-   FastAPI
-   Strawberry GraphQL
-   Redis
-   MongoDB
-   Apache Kafka
-   JWT Authentication
-   Razorpay integration
-   MongoDB Atlas full fuzzy search and autocompletion

### How to install

```sh
git clone https://github.com/glowfi/ecommerce-server
./install.sh
source ./env/bin/activate
```

### Create an .env file in the root directory

Add the below fields with your values in the `.env` file

```sh
DATABASE_URL=""
FRONTEND_URL=""
REDIS_URL=""
SECRET_KEY=""
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=7200
REFRESH_TOKEN_EXPIRE_MINUTES=14400
OTP_TOKEN_EXPIRE_MINUTES=15
MAIL_HOST=
MAIL_USERNAME=
MAIL_EMAIL=
MAIL_PASSWORD=
MAIL_PORT=
STORE_NAME=""
RAZER_KEY_ID=""
RAZER_KEY_SECRET=""
KAFKA_ORDER_TOPIC=""
KAFKA_bootstrap_servers=''
KAFKA_sasl_mechanism=''
KAFKA_security_protocol=''
KAFKA_sasl_plain_username=''
KAFKA_sasl_plain_password=''
MONGODB_ALTAS_PROJECT_ID=""
MONGODB_ALTAS_CLUSTER=""
MONGODB_ALTAS_PUBLIC_KEY=""
MONGODB_ALTAS_PRIVATE_KEY=""
MONGODB_DATABASE=""
USER_SEARCH_INDEX_NAME=""
USER_AUTOCOMPLETE_INDEX_NAME=""
TOP_RESULTS_SEARCH=6
RANDOMMER_KEY=""
```
