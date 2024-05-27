from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Characteristic(Base):
    __tablename__ = 'characteristic'

    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('component.id', ondelete='CASCADE'), nullable=False)
    attribute = Column(String, nullable=False)
    value = Column(String, nullable=False)
    component = relationship("Component", back_populates="characteristic")