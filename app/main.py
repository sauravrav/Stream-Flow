from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Event
from app.schemas import EventCreate, EventRead


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


@app.get("/events/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)) -> Event:
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

