import logging

from fastapi import FastAPI, HTTPException

from sms_antiphishing.cache.url_cache import URLCache
from sms_antiphishing.models.sms_request import SmsRequest
from sms_antiphishing.models.sms_response import SmsResponse
from sms_antiphishing.processor.sms_processor import SMSProcessor
from sms_antiphishing.service.phishing_checker import PhishingChecker
from sms_antiphishing.service.preferences_manager import PreferencesManager

app = FastAPI(
    title="SMS Anti-Phishing Service",
    description="Service for filtering phishing SMS messages",
    version="1.0.0"
)

# Initialize dependencies
cache = URLCache()
checker = PhishingChecker(cache)
pref_manager = PreferencesManager()
processor = SMSProcessor(checker, pref_manager)

@app.post("/sms", response_model=SmsResponse)
async def handle_sms(sms: SmsRequest):
    """Endpoint for processing SMS messages"""
    try:
        result = await processor.process(sms.dict())
        return result
    except Exception as e:
        logging.exception("Unhandled exception in SMS processing")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "services": ["api", "redis"]}