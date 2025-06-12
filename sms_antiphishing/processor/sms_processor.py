import logging
import re
from urllib.parse import urlparse

from sms_antiphishing.configuration.config import Config


class SMSProcessor:
    URL_PATTERN = r'https?://[^\s]+'
    COMMAND_NUMBER = Config.SERVICE_NUMBER

    def __init__(self, checker, pref_manager):
        self.checker = checker
        self.pref_manager = pref_manager

    async def process(self, sms: dict) -> dict:
        """Process SMS and return processing result"""
        try:
            # Handle command messages
            if sms["recipient"] == self.COMMAND_NUMBER:
                return self._handle_command(sms)

            # Skip processing if user hasn't opted in
            if not self.pref_manager.is_opted_in(sms["recipient"]):
                return {"status": "delivered", "reason": "User not opted in"}

            # Extract and validate URLs
            urls = self._extract_urls(sms["message"])
            if not urls:
                return {"status": "delivered", "reason": "No URLs found"}

            # Check each URL for phishing
            for url in urls:
                if not await self.checker.check_url(url):
                    logging.warning(f"Blocked phishing SMS to {sms['recipient']}")
                    return {
                        "status": "blocked",
                        "reason": f"Phishing URL detected: {url}"
                    }

            return {"status": "delivered", "reason": "All URLs safe"}

        except Exception as e:
            logging.exception("SMS processing error")
            return {"status": "error", "reason": str(e)}

    def _handle_command(self, sms: dict) -> dict:
        """Process START/STOP commands"""
        command = sms["message"].strip().upper()
        if command == "START":
            self.pref_manager.update_preference(sms["sender"], True)
            return {"status": "command_processed", "reason": "Opt-in successful"}
        elif command == "STOP":
            self.pref_manager.update_preference(sms["sender"], False)
            return {"status": "command_processed", "reason": "Opt-out successful"}
        else:
            return {"status": "invalid_command", "reason": f"Unknown command: {command}"}

    def _extract_urls(self, text: str) -> list:
        """Extract and normalize URLs from text"""
        raw_urls = re.findall(self.URL_PATTERN, text)
        return [self._normalize_url(url) for url in raw_urls]

    def _normalize_url(self, url: str) -> str:
        """Normalize URL for consistent caching"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")