from pydantic import BaseModel, ConfigDict, Field


class BrandBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre único de la marca",
        examples=["Coca-Cola"],
    )


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nuevo nombre para la marca",
        examples=["Pepsi"],
    )


class BrandRead(BrandBase):
    id: int = Field(..., description="ID único de la marca en base de datos")

    model_config = ConfigDict(from_attributes=True)
