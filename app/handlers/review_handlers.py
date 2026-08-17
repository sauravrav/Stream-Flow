from app.models import Event


def handle_review_submitted(event: Event) -> None:
    required_fields = [
        "review_id",
        "product_id",
        "user_id",
        "rating",
        "comment",
    ]
    missing_fields = [field for field in required_fields if field not in event.payload]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required review payload fields: {fields}")

    review_id = event.payload["review_id"]
    product_id = event.payload["product_id"]
    user_id = event.payload["user_id"]
    rating = event.payload["rating"]
    comment = event.payload["comment"]

    print("--------------------------------")
    print("Preparing review for moderation...")
    print(f"Review ID: {review_id}")
    print(f"Product ID: {product_id}")
    print(f"Customer ID: {user_id}")
    print(f"Rating: {rating}")
    print(f"Comment: {comment}")
    print("Review queued for moderation successfully.")
    print("--------------------------------")
