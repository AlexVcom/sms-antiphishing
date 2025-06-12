import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    WEB_RISK_API_KEY = os.getenv("WEB_RISK_API_KEY", "")
    SERVICE_NUMBER = os.getenv("SERVICE_NUMBER", "12345")
    CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", 60))
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 5))
