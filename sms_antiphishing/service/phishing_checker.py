import logging

import aiohttp

from sms_antiphishing.cache.url_cache import URLCache
from sms_antiphishing.configuration.config import Config


class PhishingChecker:
    def __init__(self, cache: URLCache = None):
        self.cache = cache or URLCache()
        self.api_key = Config.WEB_RISK_API_KEY
        self.endpoint = "https://webrisk.googleapis.com/v1eap1/evaluateUri"
        self.timeout = aiohttp.ClientTimeout(total=Config.API_TIMEOUT)

    async def check_url(self, url: str) -> bool:
        """Check if URL is safe (returns True if safe, False if phishing)"""
        cached_result = self.cache.get(url)
        if cached_result is not None:
            return cached_result

        try:
            is_phishing = await self._call_webrisk_api(url)
            self.cache.set(url, not is_phishing)
            return not is_phishing
        except Exception as e:
            logging.error(f"WebRisk API error: {str(e)}")
            return True  # Fail-safe: allow message if API fails

    async def _call_webrisk_api(self, url: str) -> bool:
        """Call WebRisk API to check URL"""
        if not self.api_key:
            logging.warning("WEB_RISK_API_KEY not set, skipping phishing check")
            return False

        params = {
            "key": self.api_key,
            "uri": url,
            "threatTypes": ["SOCIAL_ENGINEERING"]
        }

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.endpoint, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return "threat" in data