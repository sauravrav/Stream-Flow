from app.models import Event


def handle_payment_completed(event: Event) -> None:
    required_fields = ["payment_id", "user_id", "amount", "currency", "email"]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required payment payload fields: {fields}")

    payment_id = event.payload["payment_id"]
    user_id = event.payload["user_id"]
    amount = event.payload["amount"]
    currency = event.payload["currency"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing payment receipt...")
    print(f"Payment ID: {payment_id}")
    print(f"Customer ID: {user_id}")
    print(f"Amount: {currency} {amount}")
    print(f"Sending receipt to: {email}")
    print("Receipt sent successfully.")
    print("--------------------------------")

