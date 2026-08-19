from app.models import Event


def handle_loyalty_points_earned(event: Event) -> None:
    required_fields = [
        "user_id",
        "points_earned",
        "reason",
        "points_balance",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required loyalty payload fields: {fields}")

    user_id = event.payload["user_id"]
    points_earned = event.payload["points_earned"]
    reason = event.payload["reason"]
    points_balance = event.payload["points_balance"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing loyalty points notification...")
    print(f"Customer ID: {user_id}")
    print(f"Points earned: {points_earned}")
    print(f"Reason: {reason}")
    print(f"New points balance: {points_balance}")
    print(f"Sending notification to: {email}")
    print("Loyalty points notification sent successfully.")
    print("--------------------------------")
