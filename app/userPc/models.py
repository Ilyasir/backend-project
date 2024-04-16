from sqlalchemy import Column, ForeignKey, Integer
from app.database import Base

class UserPc(Base):
    __tablename__ = "user_pc"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    price = Column(Integer, nullable=False)