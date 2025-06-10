from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Not found"}})

products_list = [
        {"id": 1, "name": "Product A", "price": 10.99, "url": "https://example.com/product-a"},
        {"id": 2, "name": "Product B", "price": 20.99, "url": "https://example.com/product-b"},
        {"id": 3, "name": "Product C", "price": 30.99, "url": "https://example.com/product-c"},
        {"id": 4, "name": "Product D", "price": 40.99, "url": "https://example.com/product-d"},
        {"id": 5, "name": "Product E", "price": 50.99, "url": "https://example.com/product-e"},
    ]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def product(id: int):
    return products_list[id]