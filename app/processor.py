from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.handlers.inventory_handlers import handle_inventory_low
from app.handlers.order_handlers import handle_order_placed
from app.handlers.payment_handlers import handle_payment_completed
from app.handlers.refund_handlers import handle_refund_completed
from app.handlers.shipment_handlers import handle_shipment_dispatched
from app.handlers.user_handlers import handle_user_created
from app.models import Event

MAX_ATTEMPTS = 3

handlers = {
    "user.created": handle_user_created,
    "inventory.low": handle_inventory_low,
    "order.placed": handle_order_placed,
    "payment.completed": handle_payment_completed,
    "refund.completed": handle_refund_completed,
    "shipment.dispatched": handle_shipment_dispatched,
}


def process_next_event(db: Session) -> Event | None:
    statement = (
        select(Event)
        .where(
            Event.status == "pending",
            Event.attempt_count < MAX_ATTEMPTS,
        )
        .order_by(Event.received_at, Event.id)
        .limit(1)
    )
    event = db.scalar(statement)

    if event is None:
        return None

    event.status = "processing"
    event.attempt_count += 1
    event.error_message = None
    db.commit()

    try:
        handler = handlers.get(event.event_type)
        if handler is None:
            raise ValueError(
                f"No handler registered for event type: {event.event_type}"
            )

        handler(event)
        event.status = "completed"
        event.error_message = None
    except Exception as exc:
        event.status = (
            "dead_letter" if event.attempt_count >= MAX_ATTEMPTS else "failed"
        )
        event.error_message = str(exc)

    event.processed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(event)
    return event
