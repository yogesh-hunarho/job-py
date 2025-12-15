from pydantic import BaseModel

class SupportMessageRequest(BaseModel):
    subject: str
    message: str
    isRewrite: bool = False
