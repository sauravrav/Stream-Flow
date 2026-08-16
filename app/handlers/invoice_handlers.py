from app.models import Event


def handle_invoice_generated(event: Event) -> None:
    required_fields = [
        "invoice_id",
        "order_id",
        "amount",
        "currency",
        "due_date",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required invoice payload fields: {fields}")

    invoice_id = event.payload["invoice_id"]
    order_id = event.payload["order_id"]
    amount = event.payload["amount"]
    currency = event.payload["currency"]
    due_date = event.payload["due_date"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing invoice notification...")
    print(f"Invoice ID: {invoice_id}")
    print(f"Order ID: {order_id}")
    print(f"Amount due: {currency} {amount}")
    print(f"Due date: {due_date}")
    print(f"Sending invoice to: {email}")
    print("Invoice notification sent successfully.")
    print("--------------------------------")
