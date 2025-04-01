import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class MongoDBConfig(BaseSettings):
    mongo_user: str = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    mongo_password: str = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    mongo_host: str = os.getenv('MONGO_HOST')
    mongo_port: int = int(os.getenv('MONGO_PORT'))
    mongo_db: str = os.getenv('MONGO_DB')


class Config(BaseSettings):
    MONGO_CONFIG: MongoDBConfig = MongoDBConfig()

    class Config:
        env_file = ".env"
        extra = "allow"
