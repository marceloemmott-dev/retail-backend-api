import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating product: {e}")
        if "foreign key constraint" in str(e.orig).lower():
            raise ValueError(f"Brand with id {data.brand_id} does not exist")
        raise ValueError("Product with same SKU or code already exists")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating product: {e}")
        raise ValueError("Could not create product")

    db.refresh(product)
    return product


def list_products(db: Session) -> list[Product]:
    return db.query(Product).filter(Product.is_active == True).order_by(Product.name.asc()).all()  # noqa: E712


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()  # noqa: E712


def get_product_by_sku(db: Session, sku: str) -> Product | None:
    return db.query(Product).filter(Product.sku == sku, Product.is_active == True).first()  # noqa: E712


def get_product_by_code(db: Session, code: str) -> Product | None:
    return db.query(Product).filter(Product.code == code, Product.is_active == True).first()  # noqa: E712


def update_product(
    db: Session,
    product: Product,
    data: ProductUpdate,
) -> Product:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error updating product {product.id}: {e}")
        if "foreign key constraint" in str(e.orig).lower():
            # Note: data.brand_id might be None if not updated, but if it caused FK error it must be present
            brand_id = getattr(data, "brand_id", "unknown")
            raise ValueError(f"Brand with id {brand_id} does not exist")
        raise ValueError("Update violates unique constraints (SKU or Code already exists)")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error updating product {product.id}: {e}")
        raise ValueError("Could not update product")

    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    # Soft delete
    product.is_active = False
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting product {product.id}: {e}")
        raise ValueError("Could not delete product")
