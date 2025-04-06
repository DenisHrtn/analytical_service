import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
TOKEN_EXPIRY_MINUTES = int(os.getenv('TOKEN_EXPIRY_MINUTES'))
ALGORITHM = os.getenv('ALGORITHM')


class KafkaConsumerConfig(BaseSettings):
    kafka_bootstrap_servers: str | None = None
    kafka_topic: str | None = None


class MongoDBConfig(BaseSettings):
    mongo_user: str = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    mongo_password: str = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    mongo_host: str = os.getenv('MONGO_HOST')
    mongo_port: int = int(os.getenv('MONGO_PORT'))
    mongo_db: str = os.getenv('MONGO_INITDB_DATABASE')


class Config(BaseSettings):
    KAFKA_CONFIG: KafkaConsumerConfig = KafkaConsumerConfig()
    MONGO_CONFIG: MongoDBConfig = MongoDBConfig()

    class Config:
        env_file = ".env"
        extra = "allow"

