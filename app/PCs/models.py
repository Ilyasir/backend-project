# Здесь будут хранится: модели sqlalchemy, pydantic-схемы для валидации данных, эндпоинты
from sqlalchemy import Column, Integer, String, Boolean, JSON
from app.database import Base

class PC(Base):
    __tablename__ = "PC"
    # Столбцы
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_gaming = Column(Boolean)
    cpu_id = Column(Integer, nullable=False)
    gpu_id = Column(Integer, nullable=False)
    ram_id = Column(Integer, nullable=False)
    memory_id = Column(Integer, nullable=False)
    motherboard_id = Column(Integer, nullable=False)
    power_id = Column(Integer, nullable=False)
    user_id = Column(Integer)
    image_id = Column(Integer)    