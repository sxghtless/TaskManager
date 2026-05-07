import json
from redis import Redis
from config import get_settings

settings = get_settings()
redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

TASKS_CACHE_KEY = "tasks"
TASKS_TTL = 60 #seconds


def get_cached_tasks() -> list[dict] | None:
    data = redis_client.get(TASKS_CACHE_KEY)
    return json.loads(data) if data else None


def set_cached_tasks(tasks: list[dict]) -> None:
    redis_client.setex(TASKS_CACHE_KEY, TASKS_TTL, json.dumps(tasks))


def invalidate_tasks_cache() -> None:
    redis_client.delete(TASKS_CACHE_KEY)