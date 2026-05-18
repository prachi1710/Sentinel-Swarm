import redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Synchronous client for publishing
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def publish_event(event_type: str, data: dict):
    message = json.dumps({"type": event_type, "data": data})
    redis_client.publish("sentinel_events", message)
