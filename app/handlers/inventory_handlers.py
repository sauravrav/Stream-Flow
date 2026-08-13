from app.models import Event


def handle_inventory_low(event: Event) -> None:
    required_fields = ["sku", "product_name", "current_quantity", "reorder_level"]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required inventory payload fields: {fields}")

    sku = event.payload["sku"]
    product_name = event.payload["product_name"]
    current_quantity = event.payload["current_quantity"]
    reorder_level = event.payload["reorder_level"]

    print("--------------------------------")
    print("Preparing low inventory alert...")
    print(f"SKU: {sku}")
    print(f"Product: {product_name}")
    print(f"Current quantity: {current_quantity}")
    print(f"Reorder level: {reorder_level}")
    print("Inventory team notified successfully.")
    print("--------------------------------")
