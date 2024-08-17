import os
from dotenv import load_dotenv

from src.laboratory_service.adapters.pubsub import PubSubPublisher
from src.laboratory_service.adapters.redis import RedisPublisher
from src.laboratory_service.core.interfaces.publisher import PublisherPort

DEFAULT_REDIS_HOST = "localhost"
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_DB = 8

DEFAULT_GCP_PROJECT_ID = "bio_gcp_project"
RESULT_TOPIC = "results"


load_dotenv()


def get_publisher() -> PublisherPort:
    pub_sub_type = os.getenv("PUB_SUB_TYPE", "redis")

    if pub_sub_type == "redis":
        host = os.getenv("REDIS_HOST", DEFAULT_REDIS_HOST)
        port = int(os.getenv("REDIS_PORT", DEFAULT_REDIS_PORT))
        db = int(os.getenv("REDIS_DB", DEFAULT_REDIS_DB))
        return RedisPublisher(host=host, port=port, db=db, channel=RESULT_TOPIC)
    elif pub_sub_type == "pubsub":
        project_id = os.getenv("GCP_PROJECT_ID", DEFAULT_GCP_PROJECT_ID)
        return PubSubPublisher(project_id=project_id, topic_id=RESULT_TOPIC)
    else:
        raise ValueError("Unsupported PUB_SUB_TYPE")
