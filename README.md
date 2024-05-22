> Ecommerce server

### Technologies used:

-   FastAPI
-   Strawberry GraphQL
-   Redis
-   MongoDB

### How to install

```sh
git clone https://github.com/glowfi/ecommerce-server
./install.sh
source ./env/bin/activate
```

### Create an .env file in the root directory

Add the below fields in the `.env` file

```sh
DATABASE_URL="mongodb://localhost:27017"
REDIS_URL="redis://localhost"
SECRET_KEY="secretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
```
