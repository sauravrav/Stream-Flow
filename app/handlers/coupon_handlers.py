from app.models import Event


def handle_coupon_redeemed(event: Event) -> None:
    required_fields = [
        "coupon_code",
        "user_id",
        "order_id",
        "discount_amount",
        "currency",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required coupon payload fields: {fields}")

    coupon_code = event.payload["coupon_code"]
    user_id = event.payload["user_id"]
    order_id = event.payload["order_id"]
    discount_amount = event.payload["discount_amount"]
    currency = event.payload["currency"]

    print("--------------------------------")
    print("Recording coupon redemption...")
    print(f"Coupon code: {coupon_code}")
    print(f"Customer ID: {user_id}")
    print(f"Order ID: {order_id}")
    print(f"Discount amount: {currency} {discount_amount}")
    print("Coupon redemption recorded successfully.")
    print("--------------------------------")
