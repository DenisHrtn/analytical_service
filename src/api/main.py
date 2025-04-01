from fastapi import FastAPI

from config import Config
from containers import container, Container
from infra.services.kafka.consumer import KafkaConsumer


config = Config()
container.config.override(config)


app = FastAPI()
app.container = container


@app.on_event('startup')
async def startup_event():
    db_client = container.mongodb()

    kafka_consumer = container.kafka_consumer(db=db_client)

    await kafka_consumer.start()
    print("Kafka Consumer запущен!")
