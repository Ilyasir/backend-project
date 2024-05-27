from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('component.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="SET NULL"), nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    component = relationship('Component', back_populates='reviews')
    user = relationship('User', back_populates='reviews')