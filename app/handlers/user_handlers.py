from app.models import Event


def handle_user_created(event: Event) -> None:
    user_id = event.payload["user_id"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Sending welcome email...")
    print(f"User ID: {user_id}")
    print(f"Email: {email}")
    print("Welcome email sent successfully.")
    print("--------------------------------")

