from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from app.services import brand_service

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.post(
    "",
    response_model=BrandRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva marca",
    description="Crea una nueva marca en el sistema. El nombre debe ser único.",
    responses={
        409: {"description": "El nombre de la marca ya existe"},
    },
)
def create_brand(payload: BrandCreate, db: Session = Depends(get_db)):
    try:
        return brand_service.create_brand(db, payload.name)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[BrandRead],
    summary="Listar todas las marcas",
    description="Obtiene una lista de todas las marcas registradas, ordenadas alfabéticamente.",
)
def list_brands(db: Session = Depends(get_db)):
    return brand_service.list_brands(db)


@router.get(
    "/{brand_id}",
    response_model=BrandRead,
    summary="Obtener marca por ID",
    description="Busca y retorna una marca específica por su ID único.",
    responses={
        404: {"description": "Marca no encontrada"},
    },
)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = brand_service.get_brand_by_id(db, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand with id {brand_id} not found",
        )
    return brand


@router.put(
    "/{brand_id}",
    response_model=BrandRead,
    summary="Actualizar una marca",
    description="Actualiza el nombre de una marca existente.",
    responses={
        404: {"description": "Marca no encontrada"},
        409: {"description": "El nuevo nombre ya está en uso por otra marca"},
    },
)
def update_brand(
    brand_id: int,
    payload: BrandUpdate,
    db: Session = Depends(get_db),
):
    brand = brand_service.get_brand_by_id(db, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand with id {brand_id} not found",
        )

    try:
        return brand_service.update_brand(db, brand, payload.name)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una marca",
    description="Elimina permanentemente una marca del sistema.",
    responses={
        404: {"description": "Marca no encontrada"},
    },
)
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = brand_service.get_brand_by_id(db, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand with id {brand_id} not found",
        )

    brand_service.delete_brand(db, brand)
