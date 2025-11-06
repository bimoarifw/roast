import redis
from tasks import generate_roast

redis_cache = redis.Redis(host='redis', port=6379, db=1, decode_responses=True)

CACHE_EXPIRATION_SECONDS = 3600

def get_roast_for_name(name: str) -> str:
    """
    Orchestrates getting a roast for a given name.
    1. Checks the cache.
    2. If not in cache, queues a task for Celery to generate it.
    3. The actual result will be fetched later by the client.
    """
    cache_key = f"roast:{name.lower().strip()}"

    cached_roast = redis_cache.get(cache_key)
    if cached_roast:
        return cached_roast

    task = generate_roast.delay(name)
    
    result = task.get(timeout=45)

    redis_cache.set(cache_key, result, ex=CACHE_EXPIRATION_SECONDS)

    return result