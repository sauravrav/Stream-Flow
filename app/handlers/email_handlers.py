from app.models import Event


def handle_email_bounced(event: Event) -> None:
    required_fields = [
        "message_id",
        "email",
        "bounce_type",
        "bounce_reason",
        "occurred_at",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required email payload fields: {fields}")

    message_id = event.payload["message_id"]
    email = event.payload["email"]
    bounce_type = event.payload["bounce_type"]
    bounce_reason = event.payload["bounce_reason"]
    occurred_at = event.payload["occurred_at"]

    print("--------------------------------")
    print("Processing bounced email...")
    print(f"Message ID: {message_id}")
    print(f"Recipient: {email}")
    print(f"Bounce type: {bounce_type}")
    print(f"Bounce reason: {bounce_reason}")
    print(f"Occurred at: {occurred_at}")
    print("Email bounce recorded successfully.")
    print("--------------------------------")
