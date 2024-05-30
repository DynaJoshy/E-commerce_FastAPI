from fastapi import APIRouter, HTTPException, status
from models.product import Product
from schemas.product import product_serializer
from config.database import product_collection, product_helper
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/", response_model=product_serializer, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    product_dict = product.dict()
    new_product =   product_collection.insert_one(product_dict)
    created_product =   product_collection.find_one({"_id": new_product.inserted_id})
    return product_helper(created_product)

@router.get("/{product_id}", response_model=product_serializer)
async def get_product(product_id: str):
    product =   product_collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product_helper(product)

@router.get("/", response_model=List[product_serializer])
async def get_products():
    products =   product_collection.find().to_list(length=100)
    return [product_helper(product) for product in products]

@router.put("/{product_id}", response_model=product_serializer)
async def update_product(product_id: str, product: Product):
    existing_product =   product_collection.find_one({"_id": ObjectId(product_id)})
    if existing_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    updated_data = product.dict()
    product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": updated_data})
    updated_product =   product_collection.find_one({"_id": ObjectId(product_id)})
    return product_helper(updated_product)

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    result =   product_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully"}
