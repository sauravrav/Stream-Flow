from app.models import Event


def handle_product_price_changed(event: Event) -> None:
    required_fields = [
        "product_id",
        "product_name",
        "old_price",
        "new_price",
        "currency",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required product payload fields: {fields}")

    product_id = event.payload["product_id"]
    product_name = event.payload["product_name"]
    old_price = event.payload["old_price"]
    new_price = event.payload["new_price"]
    currency = event.payload["currency"]

    print("--------------------------------")
    print("Processing product price change...")
    print(f"Product ID: {product_id}")
    print(f"Product: {product_name}")
    print(f"Previous price: {currency} {old_price}")
    print(f"New price: {currency} {new_price}")
    print("Product price change recorded successfully.")
    print("--------------------------------")
