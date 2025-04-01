from dependency_injector import containers, providers

from infra.repos.motor.db import MongoDBClient
from config import Config, MongoDBConfig
from infra.services.kafka.consumer import KafkaConsumer


class MongoDBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=MongoDBConfig)
    mongodb = providers.Singleton(MongoDBClient, config=config)


class Container(containers.DeclarativeContainer):
    config = providers.Factory(Config)
    mongodb = providers.Container(MongoDBContainer, config=config.provided.MONGO_CONFIG)
    kafka_consumer = providers.Factory(KafkaConsumer, db=mongodb.provided.mongodb)


container = Container()
container.init_resources()
