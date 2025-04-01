import json
import asyncio

from confluent_kafka import Consumer, KafkaException
from infra.repos.motor.db import MongoDBClient

KAFKA_BROKER = "kafka:9092"
GROUP_ID = "statistics_service"
TOPICS = ["project_events", "project_member_events", "ticket_topic", "change_status_topic"]


class KafkaConsumer:
    """
    Класс для обработки событий Kafka
    """

    def __init__(self, db: MongoDBClient):
        self.db = db
        self.consumer = Consumer({
            'bootstrap.servers': KAFKA_BROKER,
            'group.id': GROUP_ID,
            'auto.offset.reset': 'earliest',
        })
        self.consumer.subscribe(topics=TOPICS)

    async def _update_user_stats(self, user_id: int, updated_data: dict):
        await self.db.user_statistics.update_one(
            {'user_id': user_id}, {'$inc': updated_data}, upsert=True
        )

    async def _handle_project_event(self, data):
        owner_id = data['owner_id']
        await self._update_user_stats(owner_id, {'projects_count': 1})

    async def _handle_project_member_event(self, data):
        user_id = data['user_id']
        await self._update_user_stats(user_id, {'members_count': 1})

    async def _handle_ticket_event(self, data):
        assignees = data['assignees_ids']
        for user_id in assignees:
            await self._update_user_stats(user_id, {'ticket_count': 1})

    async def _handle_ticket_status_change(self, data):
        new_status = data['new_status']
        old_status = data['old_status']

        update_query = {
            f'status_distribution.{old_status}': -1,
            f'status_distribution.{new_status}': 1,
        }

        await self._update_user_stats(data['project_id'], update_query)

    async def _consume_messages(self):
        handlers = {
            "project_events": self._handle_project_event,
            "project_member_events": self._handle_project_member_event,
            "ticket_topic": self._handle_ticket_event,
            "change_status_topic": self._handle_ticket_status_change,
        }

        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                await asyncio.sleep(0.5)
                continue
            if msg.error():
                raise KafkaException(msg.error())

            topic = msg.topic()
            data = json.loads(msg.value().decode("utf-8"))

            if topic in handlers:
                await handlers[topic](data)

            print(f"Обработано событие: {data}")

    async def start(self):
        asyncio.create_task(self._consume_messages())
