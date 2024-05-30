from fastapi import APIRouter, HTTPException, status
from models.user import User
from schemas.user import user_serializer
from config.database import user_collection, user_helper
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/", response_model=user_serializer, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    user_dict = user.dict()
    new_user =  user_collection.insert_one(user_dict)
    created_user =  user_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

@router.get("/{user_id}", response_model=user_serializer)
async def get_user(user_id: str):
    user =  user_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_helper(user)

@router.get("/", response_model=List[user_serializer])
async def get_users():
    users =  user_collection.find().to_list(length=100)
    return [user_helper(user) for user in users]

@router.put("/{user_id}", response_model=user_serializer)
async def update_user(user_id: str, user: User):
    existing_user =  user_collection.find_one({"_id": ObjectId(user_id)})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated_data = user.dict()
    user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
    updated_user =  user_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated_user)

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    result =  user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}
