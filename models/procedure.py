#!/usr/bin/python3
"""
    Defines the 'Procedures' class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship


class Procedure(BaseModel, Base):
    """
        Procedure class
    """
    __tablename__ = "procedures"

    name = Column(String(128), nullable=False)
    cost = Column(Float, nullable=True)
    description = Column(String(128), nullable=True)
