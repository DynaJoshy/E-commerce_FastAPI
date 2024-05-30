
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://dynajoshy:javawalispring@cluster1.njc6f6k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

database = client.ecommerce

# Collections
user_collection = database.get_collection("users")
product_collection = database.get_collection("products")
order_collection = database.get_collection("orders")

# Helpers

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
    }

def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product.get("name"),
        "description": product.get("description"),
        "price": product.get("price"),
        "quantity": product.get("quantity"),
    }

def order_helper(order) -> dict:
    return {
        "id": str(order["_id"]),
        "user_id": order.get("user_id"),
        "product_ids": order.get("product_ids"),
        "total": order.get("total"),
    }