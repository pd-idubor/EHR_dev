#!/usr/bin/python3
"""
    Defines the 'Complaint' class
"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship
# from models.history import history


class Complaint(BaseModel, Base):
    """
        Complaint class
    """
    __tablename__ = 'complaint'

    event = Column(String(128), nullable=False)
    description = Column(String(1024))
    value = Column(Float, nullable=True, default=0.0)
    user_id = Column(String(60),
                     ForeignKey('user.id'), nullable=False)
    diagnosis_id = Column(String(60),
                          ForeignKey('diagnosis.id'), nullable=False)
