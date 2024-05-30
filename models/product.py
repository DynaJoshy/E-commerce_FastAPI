from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
