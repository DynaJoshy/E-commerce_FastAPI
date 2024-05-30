from pydantic import BaseModel
from typing import List

class Order(BaseModel):
    user_id: str
    product_ids: List[str]
    total: float
