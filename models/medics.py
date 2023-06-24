#!/usr/bin/python3
"""
    Defines the 'Medications' class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Medics(BaseModel, Base):
    """
        Medics class
    """
    __tablename__ = "medics"

    name = Column(String(128), nullable=False)
    dose = Column(String(128), nullable=True)
    description = Column(String(128), nullable=True)
