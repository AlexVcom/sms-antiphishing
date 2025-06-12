import datetime
from typing import Optional

from sms_antiphishing.configuration.config import Config


class URLCache:
    def __init__(self, ttl_minutes: int = Config.CACHE_TTL_MINUTES):
        self.cache = {}
        self.ttl = datetime.timedelta(minutes=ttl_minutes)

    def get(self, url: str) -> Optional[bool]:
        entry = self.cache.get(url)
        if entry and datetime.datetime.now() < entry["expiry"]:
            return entry["is_safe"]
        return None

    def set(self, url: str, is_safe: bool):
        self.cache[url] = {
            "is_safe": is_safe,
            "expiry": datetime.datetime.now() + self.ttl
        }

    def clear(self):
        self.cache = {}