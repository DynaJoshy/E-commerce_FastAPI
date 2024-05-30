from fastapi import APIRouter, HTTPException, status
from models.order import Order
from schemas.order import order_serializer
from config.database import order_collection, order_helper
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/", response_model=order_serializer, status_code=status.HTTP_201_CREATED)
async def create_order(order: Order):
    order_dict = order.dict()
    new_order =  order_collection.insert_one(order_dict)
    created_order =  order_collection.find_one({"_id": new_order.inserted_id})
    return order_helper(created_order)

@router.get("/{order_id}", response_model=order_serializer)
async def get_order(order_id: str):
    order =  order_collection.find_one({"_id": ObjectId(order_id)})
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order_helper(order)

@router.get("/", response_model=List[order_serializer])
async def get_orders():
    orders =  order_collection.find().to_list(length=100)
    return [order_helper(order) for order in orders]

@router.put("/{order_id}", response_model=order_serializer)
async def update_order(order_id: str, order: Order):
    existing_order =  order_collection.find_one({"_id": ObjectId(order_id)})
    if existing_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    updated_data = order.dict()
    order_collection.update_one({"_id": ObjectId(order_id)}, {"$set": updated_data})
    updated_order =  order_collection.find_one({"_id": ObjectId(order_id)})
    return order_helper(updated_order)

@router.delete("/{order_id}", response_model=dict)
async def delete_order(order_id: str):
    result =  order_collection.delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"message": "Order deleted successfully"}
