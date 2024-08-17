from google.cloud import pubsub_v1

from src.patient_service.core.interfaces.subscriber import Subscriber


class PubSubSubscriber(Subscriber):
    def __init__(self, project_id: str, subscription_name: str):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_name)

    def subscribe(self) -> None:
        def callback(message):
            print(f"[pubsub subscriber] Received message: {message.data}")
            message.ack()
            # Process message

        self.subscriber.subscribe(self.subscription_path, callback=callback)
