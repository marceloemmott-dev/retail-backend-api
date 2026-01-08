from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Nombre del producto",
        examples=["Coca-Cola 1.5L"],
    )
    sku: Optional[str] = Field(
        None,
        max_length=50,
        description="SKU único del producto",
        examples=["SKU-COCA-1500"],
    )
    code: Optional[str] = Field(
        None,
        max_length=100,
        description="Código de barras único del producto",
        examples=["7801234567890"],
    )
    price: Decimal = Field(
        ...,
        description="Precio de venta del producto",
        examples=[1490.00],
    )
    brand_id: int = Field(
        ...,
        description="ID de la marca asociada",
        examples=[1],
    )
    image_url: Optional[str] = Field(
        None,
        max_length=255,
        description="URL de la imagen del producto",
        examples=["https://res.cloudinary.com/demo/image/upload/products/coca-cola.png"],
    )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=150,
        description="Nuevo nombre del producto",
    )
    sku: Optional[str] = Field(
        None,
        max_length=50,
        description="Nuevo SKU del producto",
    )
    code: Optional[str] = Field(
        None,
        max_length=100,
        description="Nuevo código de barras del producto",
    )
    price: Optional[Decimal] = Field(
        None,
        description="Nuevo precio del producto",
    )
    brand_id: Optional[int] = Field(
        None,
        description="Nuevo ID de la marca",
    )
    image_url: Optional[str] = Field(
        None,
        max_length=255,
        description="Nueva URL de la imagen",
    )
    is_active: Optional[bool] = Field(
        None,
        description="Estado activo/inactivo del producto",
    )


class ProductRead(ProductBase):
    id: int = Field(..., description="ID único del producto en base de datos")
    is_active: bool = Field(..., description="Estado activo/inactivo del producto")
    created_at: datetime = Field(..., description="Fecha de creación del producto")

    model_config = ConfigDict(from_attributes=True)
