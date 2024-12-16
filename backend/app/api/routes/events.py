from typing import Any, Sequence
from datetime import datetime

from fastapi import APIRouter, HTTPException, File, UploadFile
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Event, EventCreate, EventPublic
from app.core.config import settings
from app.crud.csv import import_csv

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventPublic)
def create_event(*, session: SessionDep, event_in: EventCreate) -> Any:
    """
    Record and events within the system.
    An event represents an interaction or action involving an item, a user, or a system-wide event, such as:
    - A user purchasing or interacting with an item.
    - A user action.
    - A general system event like.
    """
    event = Event.model_validate(event_in, update={"timestamp": datetime.now()})
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
