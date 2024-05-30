from fastapi import FastAPI
from routes.user import router as user_router
from routes.product import router as product_router
from routes.order import router as order_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
