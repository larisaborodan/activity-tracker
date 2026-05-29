"""Data models for the Activity Tracker API."""

from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field

EventType = Literal["login", "logout", "page_view", "click", "purchase"]


def _now() -> datetime:
    return datetime.now(timezone.utc)


class UserCreate(BaseModel):
    email: str
    name: str


class User(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime = Field(default_factory=_now)


class EventCreate(BaseModel):
    user_id: int
    event_type: EventType
    metadata: dict = Field(default_factory=dict)


class Event(BaseModel):
    id: int
    user_id: int
    event_type: EventType
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_now)
    deleted_at: Optional[datetime] = None
