from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Event
from app.processor import process_next_event
from app.schemas import EventCreate, EventRead, ProcessNextResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="StreamFlow", lifespan=lifespan)


@app.post("/events", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)) -> Event:
    event = Event(**event_data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@app.get("/events", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)) -> list[Event]:
    statement = select(Event).order_by(Event.id)
    return list(db.scalars(statement).all())


@app.post("/events/process-next", response_model=ProcessNextResponse)
def process_next(db: Session = Depends(get_db)) -> ProcessNextResponse:
    event = process_next_event(db)
    if event is None:
        return ProcessNextResponse(message="No pending events to process.", event=None)

    message = (
        "Event processed successfully."
        if event.status == "completed"
        else "Event processing failed."
    )
    return ProcessNextResponse(message=message, event=EventRead.model_validate(event))


@app.get("/events/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)) -> Event:
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/events/{event_id}/complete", response_model=EventRead)
def complete_event(event_id: int, db: Session = Depends(get_db)) -> Event:
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status != "pending":
        raise HTTPException(status_code=409, detail="Event is not pending")

    event.status = "completed"
    event.processed_at = datetime.now(timezone.utc)
    event.attempt_count += 1
    db.commit()
    db.refresh(event)
    return event
