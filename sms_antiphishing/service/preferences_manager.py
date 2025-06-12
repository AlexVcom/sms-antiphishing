import redis
import logging

from sms_antiphishing.configuration.config import Config


class PreferencesManager:
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                db=0,
                decode_responses=True
            )
            self.redis.ping()
        except redis.ConnectionError as e:
            logging.critical(f"Redis connection failed: {str(e)}")
            raise

    def is_opted_in(self, number: str) -> bool:
        """Check if user has opted in to phishing protection"""
        return self.redis.get(f"pref:{number}") == "true"

    def update_preference(self, number: str, preference: bool):
        """Update user preference (True = opted in)"""
        self.redis.set(f"pref:{number}", "true" if preference else "false")

    def clear_preferences(self):
        """Clear all preferences (for testing)"""
        for key in self.redis.keys("pref:*"):
            self.redis.delete(key)