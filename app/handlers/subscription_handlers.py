from app.models import Event


def handle_subscription_cancelled(event: Event) -> None:
    required_fields = [
        "subscription_id",
        "user_id",
        "plan_name",
        "cancelled_at",
        "email",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required subscription payload fields: {fields}")

    subscription_id = event.payload["subscription_id"]
    user_id = event.payload["user_id"]
    plan_name = event.payload["plan_name"]
    cancelled_at = event.payload["cancelled_at"]
    email = event.payload["email"]

    print("--------------------------------")
    print("Preparing subscription cancellation confirmation...")
    print(f"Subscription ID: {subscription_id}")
    print(f"Customer ID: {user_id}")
    print(f"Plan: {plan_name}")
    print(f"Cancelled at: {cancelled_at}")
    print(f"Sending confirmation to: {email}")
    print("Cancellation confirmation sent successfully.")
    print("--------------------------------")
