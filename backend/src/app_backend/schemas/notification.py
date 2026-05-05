import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    message: str
    user_id: uuid.UUID
    channel: str
    scheduled_at: datetime.datetime
    sent_at: Optional[datetime.datetime] = None
    status: str
