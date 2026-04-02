import json
import redis

from config.settings import REDIS_CONFIG


class CacheService:
    """
    Redis-backed cache for query results.

    Key:   fingerprint (e.g. "ecommerce:abc123...")
    Value: JSON string of {result_hash, rule_results, correct}
    """

    def __init__(self):
        self._client = None

    def connect(self):
        """Initialize Redis connection."""
        self._client = redis.Redis(
            host=REDIS_CONFIG["host"],
            port=REDIS_CONFIG["port"],
            db=REDIS_CONFIG["db"],
            decode_responses=True,
        )
        self._client.ping()
        print("Redis connected")

    def get(self, fingerprint):
        """
        Look up a cached result by fingerprint.
        Returns dict or None if cache miss.
        """
        if not self._client:
            self.connect()

        value = self._client.get(fingerprint)
        if value:
            return json.loads(value)
        return None

    def set(self, fingerprint, result, ttl=None):
        """
        Cache a result under the given fingerprint.

        Args:
            fingerprint: cache key
            result: dict with {result_hash, rule_results, correct}
            ttl: optional time-to-live in seconds
        """
        if not self._client:
            self.connect()

        payload = json.dumps(result)
        if ttl:
            self._client.setex(fingerprint, ttl, payload)
        else:
            self._client.set(fingerprint, payload)

    def delete(self, fingerprint):
        """Remove a cached entry."""
        if not self._client:
            self.connect()
        self._client.delete(fingerprint)


# Global instance
cache_service = CacheService()
