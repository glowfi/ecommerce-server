import os
import ssl
from dotenv import find_dotenv, load_dotenv
from aiokafka import AIOKafkaProducer


# Load dotenv
load_dotenv(find_dotenv(".env"))


# RedisConnection
class KafkaConnection:
    def __init__(self):
        self.KAFKA_bootstrap_servers = os.getenv("KAFKA_bootstrap_servers")
        self.KAFKA_sasl_mechanism = os.getenv("KAFKA_sasl_mechanism")
        self.KAFKA_security_protocol = os.getenv("KAFKA_security_protocol")
        self.KAFKA_sasl_plain_username = os.getenv("KAFKA_sasl_plain_username")
        self.KAFKA_sasl_plain_password = os.getenv("KAFKA_sasl_plain_password")
        self.producer = None

    async def connect(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.KAFKA_bootstrap_servers,
            sasl_mechanism=self.KAFKA_sasl_mechanism,
            security_protocol=self.KAFKA_security_protocol,
            sasl_plain_username=self.KAFKA_sasl_plain_username,
            sasl_plain_password=self.KAFKA_sasl_plain_password,
            ssl_context=ssl.create_default_context(),
        )
        # Get cluster layout and initial topic/partition leadership information
        await self.producer.start()
        print("Kafka Connected Connected!")

    async def disconnect(self):
        if self.producer:
            await self.producer.stop()
            print("Kafka Disconnected ...")


kafka_connection = KafkaConnection()
