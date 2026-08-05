from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EventCreate(BaseModel):
    event_type: str = Field(min_length=1, max_length=255)
    source: str = Field(min_length=1, max_length=255)
    payload: dict[str, Any]


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_type: str
    source: str
    payload: dict[str, Any]
    status: str
    received_at: datetime
    processed_at: datetime | None
    attempt_count: int
    error_message: str | None


class ProcessNextResponse(BaseModel):
    message: str
    event: EventRead | None
