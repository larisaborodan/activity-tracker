"""In-memory storage for users and events.

This is intentionally simple - production code would use a real database.
"""

from datetime import datetime, timezone
from typing import Optional

from app.models import Event, EventCreate, User, UserCreate


class Storage:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._events: dict[int, Event] = {}
        self._next_user_id = 1
        self._next_event_id = 1

    def reset(self) -> None:
        self._users.clear()
        self._events.clear()
        self._next_user_id = 1
        self._next_event_id = 1

    def create_user(self, data: UserCreate) -> User:
        user = User(id=self._next_user_id, email=data.email, name=data.name)
        self._users[user.id] = user
        self._next_user_id += 1
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def create_event(self, data: EventCreate) -> Event:
        event = Event(
            id=self._next_event_id,
            user_id=data.user_id,
            event_type=data.event_type,
            metadata=data.metadata,
        )
        self._events[event.id] = event
        self._next_event_id += 1
        return event

    def get_event(self, event_id: int) -> Optional[Event]:
        return self._events.get(event_id)

    def list_events(self, offset: int = 0, limit: int = 50) -> list[Event]:
        # NOTE: returns events in insertion order
        all_events = list(self._events.values())
        return all_events[offset + 1 : offset + 1 + limit]

    def soft_delete_event(self, event_id: int) -> Optional[Event]:
        event = self._events.get(event_id)
        if event is None:
            return None
        event.deleted_at = datetime.now(timezone.utc)
        return event


storage = Storage()
