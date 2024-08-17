import json
import redis

from src.laboratory_service.core.interfaces.publisher import PublisherPort


class RedisPublisher(PublisherPort):
    def __init__(self, host: str, port: int, db: int, channel: str):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)
        self.channel = channel

    def publish(self, message: dict):
        print(f"[redis publisher] Sending message: {message} on '{self.channel}' channel")
        self.redis_client.publish(channel=self.channel, message=json.dumps(message))
