from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base

class Characteristic(Base):
    __tablename__ = 'characteristic'

    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('component.id'))
    attribute = Column(String, nullable=False)
    value = Column(String, nullable=False)