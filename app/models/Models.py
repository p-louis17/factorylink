from sqlalchemy import Column, String, Float, Boolean, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum, uuid

Base = declarative_base()

def gen_id():
    return str(uuid.uuid4())

class RoleEnum(str, enum.Enum):
    supplier = "supplier"
    manufacturer = "manufacturer"
    admin = "admin"

class StatusEnum(str, enum.Enum):
    draft = "draft"
    pending = "pending"
    matched = "matched"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    declined = "declined"

class ListingStatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class User(Base):
    __tablename__ = "users"
    user_id     = Column(String, primary_key=True, default=gen_id)
    name        = Column(String, nullable=False)
    email       = Column(String, unique=True, nullable=False)
    password    = Column(String, nullable=False)
    role        = Column(Enum(RoleEnum), nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    supplier_profile     = relationship("Supplier", back_populates="user", uselist=False)
    manufacturer_profile = relationship("Manufacturer", back_populates="user", uselist=False)

class Supplier(Base):
    __tablename__ = "suppliers"
    supplier_id    = Column(String, primary_key=True, default=gen_id)
    user_id        = Column(String, ForeignKey("users.user_id"), unique=True)
    company_name   = Column(String, nullable=False)
    location       = Column(String)
    material_types = Column(String)   
    rating         = Column(Float, default=0.0)

    user     = relationship("User", back_populates="supplier_profile")
    listings = relationship("MaterialListing", back_populates="supplier")

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    manufacturer_id     = Column(String, primary_key=True, default=gen_id)
    user_id             = Column(String, ForeignKey("users.user_id"), unique=True)
    factory_name        = Column(String, nullable=False)
    industry            = Column(String)
    production_capacity = Column(String)
    location            = Column(String)

    user     = relationship("User", back_populates="manufacturer_profile")
    requests = relationship("MaterialRequest", back_populates="manufacturer")

class MaterialListing(Base):
    __tablename__ = "material_listings"
    listing_id      = Column(String, primary_key=True, default=gen_id)
    supplier_id     = Column(String, ForeignKey("suppliers.supplier_id"))
    material_name   = Column(String, nullable=False)
    quantity        = Column(Float, nullable=False)
    unit            = Column(String, nullable=False)
    price_per_unit  = Column(Float, nullable=False)
    status          = Column(Enum(ListingStatusEnum), default=ListingStatusEnum.active)
    description     = Column(Text)
    created_at      = Column(DateTime, default=datetime.utcnow)

    supplier  = relationship("Supplier", back_populates="listings")
    requests  = relationship("MaterialRequest", back_populates="listing")

class MaterialRequest(Base):
    __tablename__ = "material_requests"
    request_id      = Column(String, primary_key=True, default=gen_id)
    manufacturer_id = Column(String, ForeignKey("manufacturers.manufacturer_id"))
    listing_id      = Column(String, ForeignKey("material_listings.listing_id"), nullable=True)
    material_name   = Column(String, nullable=False)
    quantity        = Column(Float, nullable=False)
    unit            = Column(String, nullable=False)
    price_per_unit  = Column(Float, nullable=True)
    status          = Column(Enum(StatusEnum), default=StatusEnum.draft)
    created_at      = Column(DateTime, default=datetime.utcnow)

    manufacturer = relationship("Manufacturer", back_populates="requests")
    listing      = relationship("MaterialListing", back_populates="requests")
    notification = relationship("Notification", back_populates="request", uselist=False)

class Notification(Base):
    __tablename__ = "notifications"
    notif_id     = Column(String, primary_key=True, default=gen_id)
    recipient_id = Column(String, ForeignKey("users.user_id"))
    request_id   = Column(String, ForeignKey("material_requests.request_id"))
    message      = Column(String)
    is_read      = Column(Boolean, default=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

    request = relationship("MaterialRequest", back_populates="notification")
