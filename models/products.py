from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str
    sku: str


class UpdateProductRequest(BaseModel):
    name: str
    price: float
    description: str


class GetProductsResponse(BaseModel):
    products: List[Product]


class CreateProductResponse(BaseModel):
    message: str


class DeleteProductResponse(BaseModel):
    message: str


class UpdateProductResponse(BaseModel):
    message: str
