from app.models import Event


def handle_order_placed(event: Event) -> None:
    required_fields = [
        "order_id",
        "user_id",
        "items",
        "total",
        "currency",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required order payload fields: {fields}")

    order_id = event.payload["order_id"]
    user_id = event.payload["user_id"]
    items = event.payload["items"]
    total = event.payload["total"]
    currency = event.payload["currency"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing order confirmation...")
    print(f"Order ID: {order_id}")
    print(f"Customer ID: {user_id}")
    print(f"Number of items: {len(items)}")
    print(f"Order total: {currency} {total}")
    print(f"Sending confirmation to: {email}")
    print("Order confirmation sent successfully.")
    print("--------------------------------")
