from app.models import Event


def handle_return_requested(event: Event) -> None:
    required_fields = [
        "return_id",
        "order_id",
        "user_id",
        "items",
        "reason",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required return payload fields: {fields}")

    return_id = event.payload["return_id"]
    order_id = event.payload["order_id"]
    user_id = event.payload["user_id"]
    items = event.payload["items"]
    reason = event.payload["reason"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing return request...")
    print(f"Return ID: {return_id}")
    print(f"Order ID: {order_id}")
    print(f"Customer ID: {user_id}")
    print(f"Number of items: {len(items)}")
    print(f"Reason: {reason}")
    print(f"Sending return instructions to: {email}")
    print("Return request created successfully.")
    print("--------------------------------")
