from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.components.characteristics.models import Characteristic
from app.components.reviews.models import Review

class Component(Base):
    __tablename__ = "component"

    id = Column(Integer, primary_key=True)
    type = Column(Enum('cpu', 'gpu', 'mb', 'ram', 'memory', 'power', 'cooler', 'case', name='component_types'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String)
    image_path = Column(String)
    characteristic = relationship("Characteristic", back_populates="component", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="component", cascade="all, delete-orphan")