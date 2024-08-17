import json
import redis

from src.patient_service.core.interfaces.subscriber import Subscriber
from src.patient_service.core.services.database import record_test


class RedisSubscriber(Subscriber):
    def __init__(self, host: str, port: int, db: int, channel: str):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)
        self.channel = channel

    def subscribe(self) -> None:
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(self.channel)
        for message in pubsub.listen():
            if message and message['type'] == 'message':
                print(f"[redis subscriber] Received message: {message['data']}")
                record_test(json.loads(message["data"]))
