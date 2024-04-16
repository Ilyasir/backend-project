from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from app.database import Base

class Component(Base):
    __tablename__ = "component"

    id = Column(Integer, primary_key=True)
    pc_id = Column(Integer, ForeignKey("user_pc.id"))
    type = Column(Enum('cpu', 'gpu', 'motherboard','ram', 'memory', 'power', 'cooler', 'case', name='component_types'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(String, nullable=False)
    image_path = Column(String, nullable=True)