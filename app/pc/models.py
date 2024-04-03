# Здесь будут хранится: модели sqlalchemy, pydantic-схемы для валидации данных, эндпоинты
from sqlalchemy import Column, ForeignKey, Integer, Float, String, Boolean
from app.database import Base

# Таблица с готовыми сборками
class pc(Base):
    __tablename__ = "pc"
    # Столбцы
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_gaming = Column(Boolean)
    cpu_id = Column(ForeignKey("cpu.id"))
    user_id = Column(ForeignKey("user.id"))
    image_id = Column(Integer)

# Таблица с характеристиками процессора
class cpu(Base):
    __tablename__ = "cpu"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    socket = Column(String, nullable=False)
    model = Column(String, nullable=False)
    core = Column(Integer, nullable=False)
    techprocess = Column(Integer, nullable=False)
    frequency = Column(Float, nullable=False)
    is_videocore = Column(Boolean, nullable=False)
    price = Column(Integer, nullable=False)
    image_id = Column(Integer)