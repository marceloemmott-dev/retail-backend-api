from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto",
    description=(
        "Crea un nuevo producto en el catálogo. El nombre, precio y marca son " "obligatorios. SKU y código deben ser únicos."
    ),
    responses={
        409: {"description": "El SKU o código ya existe"},
    },
)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    try:
        return product_service.create_product(db, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[ProductRead],
    summary="Listar todos los productos",
    description="Obtiene una lista de todos los productos registrados en el sistema, ordenados por nombre.",
)
def list_products(db: Session = Depends(get_db)):
    return product_service.list_products(db)


@router.get(
    "/sku/{sku}",
    response_model=ProductRead,
    summary="Obtener producto por SKU",
    description="Busca y retorna un producto específico por su código SKU.",
    responses={
        404: {"description": "Producto no encontrado"},
    },
)
def get_product_by_sku(sku: str, db: Session = Depends(get_db)):
    product = product_service.get_product_by_sku(db, sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with sku {sku} not found",
        )
    return product


@router.get(
    "/code/{code}",
    response_model=ProductRead,
    summary="Obtener producto por Código de Barras",
    description="Busca y retorna un producto específico por su código de barras.",
    responses={
        404: {"description": "Producto no encontrado"},
    },
)
def get_product_by_code(code: str, db: Session = Depends(get_db)):
    product = product_service.get_product_by_code(db, code)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with code {code} not found",
        )
    return product


@router.get(
    "/{product_id}",
    response_model=ProductRead,
    summary="Obtener producto por ID",
    description="Busca y retorna un producto específico por su ID único.",
    responses={
        404: {"description": "Producto no encontrado"},
    },
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return product


@router.put(
    "/{product_id}",
    response_model=ProductRead,
    summary="Actualizar un producto",
    description="Actualiza los datos de un producto existente. Solo se modifican los campos enviados.",
    responses={
        404: {"description": "Producto no encontrado"},
        409: {"description": "El nuevo SKU o código ya está en uso"},
    },
)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )

    try:
        return product_service.update_product(db, product, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un producto",
    description=(
        "Marca el producto como inactivo (borrado lógico), por lo que ya no "
        "aparecerá en listados pero se mantendrá en el historial."
    ),
    responses={
        404: {"description": "Producto no encontrado"},
    },
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )

    try:
        product_service.delete_product(db, product)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
