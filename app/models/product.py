from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    sku = Column(String(50), unique=True, nullable=True)
    code = Column(String(100), unique=True, nullable=True)

    price = Column(Numeric(10, 2), nullable=False)

    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)

    image_url = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    brand = relationship("Brand", backref="products")
