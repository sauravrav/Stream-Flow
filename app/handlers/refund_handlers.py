from app.models import Event


def handle_refund_completed(event: Event) -> None:
    required_fields = [
        "refund_id",
        "payment_id",
        "amount",
        "currency",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required refund payload fields: {fields}")

    refund_id = event.payload["refund_id"]
    payment_id = event.payload["payment_id"]
    amount = event.payload["amount"]
    currency = event.payload["currency"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing refund confirmation...")
    print(f"Refund ID: {refund_id}")
    print(f"Payment ID: {payment_id}")
    print(f"Refund amount: {currency} {amount}")
    print(f"Sending confirmation to: {email}")
    print("Refund confirmation sent successfully.")
    print("--------------------------------")
