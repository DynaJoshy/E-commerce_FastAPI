def order_serializer(todo) -> dict:
    return {
        "_id": str(todo["_id"]),  # Ensure ObjectId is converted to string
        "name": todo.get("name", ""),  # Use .get() to safely access dictionary keys
        "description": todo.get("description", ""),
        "completed": todo.get("completed", False)  # Assuming default value for completed is False
    }

def todos_serializer(todos) -> list:
    return [order_serializer(todo) for todo in todos]