from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ReadyPc(Base):
    __tablename__ = "ready_pc"

    id = Column(Integer, primary_key=True)
    name = Column(String , nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String)
    image_path = Column(String)
    components = relationship("Component", secondary="ready_pc_component")

class ReadyPcComponent(Base):
    __tablename__ = "ready_pc_component"

    id = Column(Integer, primary_key=True)
    ready_pc_id = Column(Integer, ForeignKey("ready_pc.id"))
    component_id = Column(Integer, ForeignKey("component.id"))