from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class WebhookPayload(BaseModel):
    event_id: str
    type: str
    data: Dict[str, Any]

class WebhookOut(BaseModel):
    event_id: str
    payload: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ Pydantic v2

class WebhookResponse(BaseModel):
    status: str
    message: str
