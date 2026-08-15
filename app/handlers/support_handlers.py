from app.models import Event


def handle_support_ticket_created(event: Event) -> None:
    required_fields = [
        "ticket_id",
        "user_id",
        "subject",
        "priority",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required support payload fields: {fields}")

    ticket_id = event.payload["ticket_id"]
    user_id = event.payload["user_id"]
    subject = event.payload["subject"]
    priority = event.payload["priority"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Routing new support ticket...")
    print(f"Ticket ID: {ticket_id}")
    print(f"Customer ID: {user_id}")
    print(f"Subject: {subject}")
    print(f"Priority: {priority}")
    print(f"Sending acknowledgement to: {email}")
    print("Support ticket routed successfully.")
    print("--------------------------------")
