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
        all_events = [e for e in self._events.values() if e.deleted_at is None]
        return all_events[offset  : offset  + limit]
    
    def get_user_events(
        self,
        user_id: int,
        since: Optional[datetime] = None,
    ) -> list[Event]:
        events = [
            e for e in self._events.values()
            if e.user_id == user_id
            and e.deleted_at is None
            and (since is None or e.created_at > since)
        ]
        return sorted(events, key=lambda e: e.created_at)

    def soft_delete_event(self, event_id: int) -> Optional[Event]:
        event = self._events.get(event_id)
        if event is None:
            return None
        if event.deleted_at is not None:
            return None
        event.deleted_at = datetime.now(timezone.utc)
        return event


storage = Storage()
