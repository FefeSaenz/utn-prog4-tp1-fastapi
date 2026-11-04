from fastapi import APIRouter, HTTPException, status
from models.products import (
    Product,
    UpdateProductRequest,
    GetProductsResponse,
    CreateProductResponse,
    DeleteProductResponse,
    UpdateProductResponse,
)

router = APIRouter()

productos: list[Product] = [
    Product(id=1, name="Remera Negra", price=25000.0, description="Remera 100% algodón", sku="SKU001"),
    Product(id=2, name="Remera Blanca", price=25000.0, description="Remera 100% algodón", sku="SKU002"),
    Product(id=3, name="Pantalón Cargo", price=35000.0, description="Oversize", sku="SKU003"),
    Product(id=4, name="Jean Celeste", price=30000.0, description="Oversize", sku="SKU004")
]


@router.get("/product")
def get_products(name: str | None = None) -> GetProductsResponse:
    # Si no se pasa el query param name, devuelve todos los productos
    if not name:
        return GetProductsResponse(products=productos)

    # Crea una lista nueva solo con los productos cuyo nombre contiene la cadena pasada
    filtrados = [product for product in productos if name.lower() in product.name.lower()]
    return GetProductsResponse(products=filtrados)


@router.post("/product", status_code=status.HTTP_201_CREATED)
def create_product(product: Product) -> CreateProductResponse:
    # Si el id ya existe, devuelve un 409 y no agrega el producto
    for existing_product in productos:
        if existing_product.id == product.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un producto con ese id"
            )

    productos.append(product)
    return CreateProductResponse(message="producto creado")


@router.get("/product/{id}")
def get_product_by_id(id: int) -> Product:
    for product in productos:
        if product.id == id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado"
    )


@router.put("/product/{id}")
def update_product(id: int, datos: UpdateProductRequest) -> UpdateProductResponse:
    for product in productos:
        if product.id == id:
            product.name = datos.name
            product.price = datos.price
            product.description = datos.description
            return UpdateProductResponse(message="producto actualizado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado"
    )


@router.delete("/product/{id}")
def delete_product(id: int) -> DeleteProductResponse:
    for product in productos:
        if product.id == id:
            productos.remove(product)
            return DeleteProductResponse(message="producto borrado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado"
    )
