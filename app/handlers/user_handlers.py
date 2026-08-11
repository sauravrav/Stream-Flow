from app.models import Event


def handle_user_created(event: Event) -> None:
    required_fields = ["user_id", "email"]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required user payload fields: {fields}")

    user_id = event.payload["user_id"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Sending welcome email...")
    print(f"User ID: {user_id}")
    print(f"Email: {email}")
    print("Welcome email sent successfully.")
    print("--------------------------------")
