from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.brand import Brand


def create_brand(db: Session, name: str) -> Brand:
    brand = Brand(name=name)
    db.add(brand)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Brand with this name already exists")

    db.refresh(brand)
    return brand


def list_brands(db: Session) -> list[Brand]:
    return db.query(Brand).order_by(Brand.name.asc()).all()


def get_brand_by_id(db: Session, brand_id: int) -> Brand | None:
    return db.get(Brand, brand_id)


def update_brand(db: Session, brand: Brand, name: str | None) -> Brand:
    if name is not None:
        brand.name = name

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Brand with this name already exists")

    db.refresh(brand)
    return brand


def delete_brand(db: Session, brand: Brand) -> None:
    db.delete(brand)
    db.commit()
