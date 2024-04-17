from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from app.components.models import Component

class UserPc(Base):
    __tablename__ = "user_pc"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    price = Column(Integer, nullable=False)
    user = relationship("User", back_populates="user_pc")
    components = relationship("Component", secondary="user_pc_component")

class UserPcComponent(Base):
    __tablename__ = "user_pc_component"

    id = Column(Integer, primary_key=True)
    user_pc_id = Column(Integer, ForeignKey("user_pc.id"))
    component_id = Column(Integer, ForeignKey("component.id"))