from app.models import Event


def handle_suspicious_login(event: Event) -> None:
    required_fields = [
        "user_id",
        "ip_address",
        "location",
        "occurred_at",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required login payload fields: {fields}")

    user_id = event.payload["user_id"]
    ip_address = event.payload["ip_address"]
    location = event.payload["location"]
    occurred_at = event.payload["occurred_at"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing suspicious login alert...")
    print(f"User ID: {user_id}")
    print(f"IP address: {ip_address}")
    print(f"Location: {location}")
    print(f"Occurred at: {occurred_at}")
    print(f"Sending security alert to: {email}")
    print("Suspicious login alert sent successfully.")
    print("--------------------------------")
