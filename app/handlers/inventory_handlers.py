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


def handle_inventory_restocked(event: Event) -> None:
    required_fields = [
        "sku",
        "product_name",
        "quantity_added",
        "new_quantity",
        "warehouse_id",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required restock payload fields: {fields}")

    sku = event.payload["sku"]
    product_name = event.payload["product_name"]
    quantity_added = event.payload["quantity_added"]
    new_quantity = event.payload["new_quantity"]
    warehouse_id = event.payload["warehouse_id"]

    print("--------------------------------")
    print("Recording inventory restock...")
    print(f"SKU: {sku}")
    print(f"Product: {product_name}")
    print(f"Quantity added: {quantity_added}")
    print(f"New quantity: {new_quantity}")
    print(f"Warehouse ID: {warehouse_id}")
    print("Inventory restock recorded successfully.")
    print("--------------------------------")
