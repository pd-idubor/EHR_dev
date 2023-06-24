#!/usr/bin/python3
"""
    Defines the 'Demographics' class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Demo(BaseModel, Base):
    """
        Demo class
    """
    __tablename__ = "demo"

    gender = Column(String(128), nullable=False)
    address = Column(String(1024))
    marital_status = Column(String(128))
    age = Column(Integer(), default=0)
    user = relationship("User", backref="demo",
                        cascade="all, delete, delete-orphan")
