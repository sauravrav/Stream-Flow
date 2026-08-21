from app.models import Event


def handle_gift_card_redeemed(event: Event) -> None:
    required_fields = [
        "gift_card_id",
        "user_id",
        "order_id",
        "amount",
        "currency",
        "remaining_balance",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required gift card payload fields: {fields}")

    gift_card_id = event.payload["gift_card_id"]
    user_id = event.payload["user_id"]
    order_id = event.payload["order_id"]
    amount = event.payload["amount"]
    currency = event.payload["currency"]
    remaining_balance = event.payload["remaining_balance"]

    print("--------------------------------")
    print("Recording gift card redemption...")
    print(f"Gift card ID: {gift_card_id}")
    print(f"Customer ID: {user_id}")
    print(f"Order ID: {order_id}")
    print(f"Amount redeemed: {currency} {amount}")
    print(f"Remaining balance: {currency} {remaining_balance}")
    print("Gift card redemption recorded successfully.")
    print("--------------------------------")
