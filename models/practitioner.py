#!/usr/bin/python3
"""
    Defines the 'Demographics' class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Practitioner(BaseModel, Base):
    """
        Practitioner class
    """
    __tablename__ = "practitioner"

    name = Column(String(128), nullable=False)
    practice = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    license = Column(String(128), nullable=False)
    gender = Column(String(128), nullable=True)
    address = Column(String(1024))
    marital_status = Column(String(128))
    age = Column(Integer(), default=0)
    user = relationship("User", backref="practitioner",
                        cascade="all, delete, delete-orphan")
