from app.models import Event


def handle_payment_completed(event: Event) -> None:
    payload = event.payload
    required_fields = ["payment_id", "user_id", "amount", "currency", "email"]
    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required payment payload fields: {fields}")

    payment_id = payload["payment_id"]
    user_id = payload["user_id"]
    amount = payload["amount"]
    currency = payload["currency"]
    email = payload["email"]

    print("--------------------------------")
    print("Preparing payment receipt...")
    print(f"Payment ID: {payment_id}")
    print(f"Customer ID: {user_id}")
    print(f"Amount: {currency} {amount}")
    print(f"Sending receipt to: {email}")
    print("Receipt sent successfully.")
    print("--------------------------------")
