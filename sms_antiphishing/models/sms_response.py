from pydantic import BaseModel


class SmsResponse(BaseModel):
    status: str
    reason: str = ""