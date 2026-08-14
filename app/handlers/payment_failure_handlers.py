from app.models import Event


def handle_payment_failed(event: Event) -> None:
    required_fields = [
        "payment_id",
        "user_id",
        "amount",
        "currency",
        "failure_reason",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required payment failure payload fields: {fields}")

    payment_id = event.payload["payment_id"]
    user_id = event.payload["user_id"]
    amount = event.payload["amount"]
    currency = event.payload["currency"]
    failure_reason = event.payload["failure_reason"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing payment failure notification...")
    print(f"Payment ID: {payment_id}")
    print(f"Customer ID: {user_id}")
    print(f"Attempted amount: {currency} {amount}")
    print(f"Failure reason: {failure_reason}")
    print(f"Sending notification to: {email}")
    print("Payment failure notification sent successfully.")
    print("--------------------------------")
