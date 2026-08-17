from app.models import Event


def handle_cart_abandoned(event: Event) -> None:
    required_fields = [
        "cart_id",
        "user_id",
        "items",
        "abandoned_at",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required cart payload fields: {fields}")

    cart_id = event.payload["cart_id"]
    user_id = event.payload["user_id"]
    items = event.payload["items"]
    abandoned_at = event.payload["abandoned_at"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing abandoned cart reminder...")
    print(f"Cart ID: {cart_id}")
    print(f"Customer ID: {user_id}")
    print(f"Number of items: {len(items)}")
    print(f"Abandoned at: {abandoned_at}")
    print(f"Sending reminder to: {email}")
    print("Abandoned cart reminder sent successfully.")
    print("--------------------------------")
