from app.models import Event


def handle_wishlist_item_added(event: Event) -> None:
    required_fields = [
        "wishlist_id",
        "user_id",
        "product_id",
        "product_name",
        "added_at",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required wishlist payload fields: {fields}")

    wishlist_id = event.payload["wishlist_id"]
    user_id = event.payload["user_id"]
    product_id = event.payload["product_id"]
    product_name = event.payload["product_name"]
    added_at = event.payload["added_at"]

    print("--------------------------------")
    print("Recording wishlist activity...")
    print(f"Wishlist ID: {wishlist_id}")
    print(f"Customer ID: {user_id}")
    print(f"Product ID: {product_id}")
    print(f"Product: {product_name}")
    print(f"Added at: {added_at}")
    print("Wishlist activity recorded successfully.")
    print("--------------------------------")
