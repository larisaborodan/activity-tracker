"""Activity Tracker API.

A small FastAPI service for tracking user activity events.
"""

from fastapi import FastAPI, HTTPException, Query

from app.models import Event, EventCreate, User, UserCreate
from app.storage import storage

app = FastAPI(title="Activity Tracker API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/users", response_model=User, status_code=201)
def create_user(data: UserCreate) -> User:
    return storage.create_user(data)


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    user = storage.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/events", response_model=Event)
def create_event(data: EventCreate) -> Event:
    user = storage.get_user(data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return storage.create_event(data)


@app.get("/events", response_model=list[Event])
def list_events(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> list[Event]:
    return storage.list_events(offset=offset, limit=limit)


@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: int) -> None:
    event = storage.soft_delete_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return None
