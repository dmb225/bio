import os
from dotenv import load_dotenv

from src.patient_service.adapters.pubsub import PubSubSubscriber
from src.patient_service.adapters.redis import RedisSubscriber
from src.patient_service.core.interfaces.subscriber import Subscriber

DEFAULT_REDIS_HOST = "localhost"
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_DB = 8

DEFAULT_GCP_PROJECT_ID = "bio_gcp_project"


load_dotenv()


def get_subscriber(topic: str) -> Subscriber:
    pub_sub_type = os.getenv("PUB_SUB_TYPE", "redis")

    if pub_sub_type == "redis":
        host = os.getenv("REDIS_HOST", DEFAULT_REDIS_HOST)
        port = int(os.getenv("REDIS_PORT", DEFAULT_REDIS_PORT))
        db = int(os.getenv("REDIS_DB", DEFAULT_REDIS_DB))
        return RedisSubscriber(host=host, port=port, db=db, channel=topic)
    elif pub_sub_type == "pubsub":
        project_id = os.getenv("GCP_PROJECT_ID", DEFAULT_GCP_PROJECT_ID)
        return PubSubSubscriber(project_id=project_id, subscription_name=topic)
    else:
        raise ValueError("Unsupported PUB_SUB_TYPE")
