from pydantic import BaseModel


class SmsRequest(BaseModel):
    sender: str
    recipient: str
    message: str
