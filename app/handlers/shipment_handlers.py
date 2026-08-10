from app.models import Event


def handle_shipment_dispatched(event: Event) -> None:
    required_fields = [
        "shipment_id",
        "order_id",
        "carrier",
        "tracking_number",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required shipment payload fields: {fields}")

    shipment_id = event.payload["shipment_id"]
    order_id = event.payload["order_id"]
    carrier = event.payload["carrier"]
    tracking_number = event.payload["tracking_number"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing shipment notification...")
    print(f"Shipment ID: {shipment_id}")
    print(f"Order ID: {order_id}")
    print(f"Carrier: {carrier}")
    print(f"Tracking number: {tracking_number}")
    print(f"Sending notification to: {email}")
    print("Shipment notification sent successfully.")
    print("--------------------------------")
