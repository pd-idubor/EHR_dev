#!/usr/bin/python3
"""
    Defines the 'Diagnosis' class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.complaint import Complaint
from models.user import User


class Diagnosis(BaseModel, Base):
    """
        Diagnosis class
    """
    __tablename__ = "diagnosis"

    name = Column(String(128), nullable=False)
    text = Column(String(1056), nullable=True)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    complaint = relationship("Complaint", backref="diagnosis",
                             cascade="all, delete, delete-orphan")
