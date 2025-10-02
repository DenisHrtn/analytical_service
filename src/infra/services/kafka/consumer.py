import asyncio
import json

from aiokafka import AIOKafkaConsumer
from application.events.check_events import CheckEventsDriver
from config import KafkaConsumerConfig


class KafkaConsumer:
    def __init__(
            self,
            config: KafkaConsumerConfig,
            check_events_driver: CheckEventsDriver
    ):
        self.consumer = AIOKafkaConsumer(
            config.kafka_topic,
            bootstrap_servers=config.kafka_bootstrap_servers,
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
            group_id=None,
            auto_offset_reset='earliest'
        )
        self._check_events_driver = check_events_driver

    async def start(self):
        await self.consumer.start()
        asyncio.create_task(self.consume())

    async def stop(self):
        await self.consumer.stop()

    async def consume(self):
        try:
            async for message in self.consumer:
                await self._check_events_driver.check_events(message.value)
        except Exception as e:
            await self.stop()
