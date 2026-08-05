from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status as http_status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Event
from app.processor import MAX_ATTEMPTS, process_next_event
from app.schemas import (
    EventCreate,
    EventRead,
    EventStats,
    ProcessNextResponse,
    RetryResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="StreamFlow", lifespan=lifespan)


@app.post(
    "/events", response_model=EventRead, status_code=http_status.HTTP_201_CREATED
)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)) -> Event:
    event = Event(**event_data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@app.get("/events", response_model=list[EventRead])
def list_events(
    db: Session = Depends(get_db),
    status: str | None = None,
    event_type: str | None = None,
) -> list[Event]:
    statement = select(Event).order_by(Event.id)
    if status is not None:
        statement = statement.where(Event.status == status)
    if event_type is not None:
        statement = statement.where(Event.event_type == event_type)
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


@app.get("/events/stats", response_model=EventStats)
def event_stats(db: Session = Depends(get_db)) -> EventStats:
    statement = select(Event.status, func.count(Event.id)).group_by(Event.status)
    counts = dict(db.execute(statement).all())

    return EventStats(
        total=sum(counts.values()),
        pending=counts.get("pending", 0),
        processing=counts.get("processing", 0),
        completed=counts.get("completed", 0),
        failed=counts.get("failed", 0),
    )


@app.get("/events/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)) -> Event:
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/events/{event_id}/retry", response_model=RetryResponse)
def retry_event(event_id: int, db: Session = Depends(get_db)) -> RetryResponse:
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status != "failed":
        raise HTTPException(status_code=400, detail="Only failed events can be retried.")
    if event.attempt_count >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=400,
            detail="Event has reached the maximum number of processing attempts.",
        )

    event.status = "pending"
    event.error_message = None
    event.processed_at = None
    db.commit()
    db.refresh(event)

    return RetryResponse(
        message="Event is pending and ready to be processed again.",
        event=EventRead.model_validate(event),
    )


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
