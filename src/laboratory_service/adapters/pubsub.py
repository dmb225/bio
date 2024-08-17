import json
from google.cloud import pubsub_v1

from src.laboratory_service.core.interfaces.publisher import PublisherPort


class PubSubPublisher(PublisherPort):
    def __init__(self, project_id: str, topic_id: str):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def publish(self, message: dict):
        print(f"[pubsub publisher] Sending message: {message}")
        data = json.dumps(message).encode("utf-8")
        self.publisher.publish(self.topic_path, data)
