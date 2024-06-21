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
ACCESS_TOKEN_EXPIRE_MINUTES=
ALGORITHM=""
DATABASE_URL=""
FRONTEND_URL=""
KAFKA_bootstrap_servers=""
KAFKA_ORDER_TOPIC=""
KAFKA_sasl_mechanism=""
KAFKA_sasl_plain_password=""
KAFKA_sasl_plain_username=""
KAFKA_security_protocol=""
MAIL_EMAIL=""
MAIL_HOST=""
MAIL_PASSWORD=""
MAIL_PORT=587
MAIL_USERNAME=""
MONGODB_ALTAS_CLUSTER=""
MONGODB_ALTAS_PRIVATE_KEY=""
MONGODB_ALTAS_PROJECT_ID=""
MONGODB_ALTAS_PUBLIC_KEY=""
MONGODB_DATABASE=""
OTP_TOKEN_EXPIRE_MINUTES=1440
RANDOMMER_KEY=""
RAZORPAY_KEY_ID=""
RAZORPAY_KEY_SECRET=""
REDIS_URL=""
REFRESH_TOKEN_EXPIRE_MINUTES=14400
RENDER_EXTERNAL_HOSTNAME=""
RENDER_EXTERNAL_URL=""
SECRET_KEY=""
SECRET_REQ_RES=""
STAGE=""
STORE_NAME=""
TOP_RESULTS_SEARCH=6
USER_AUTOCOMPLETE_INDEX_NAME=""
USER_SEARCH_INDEX_NAME=""
```
