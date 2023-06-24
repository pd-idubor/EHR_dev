#!/usr/bin/python3
"""
    Defines the 'Labs' class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship


class Labs(BaseModel, Base):
    """
        Labs class
    """
    __tablename__ = "labs"

    FBS = Column(Float, nullable=True, default=0.0)
    BP = Column(Float, nullable=True, default=0.0)
    WBC = Column(Float, nullable=True, default=0.0)
    RBC = Column(Float, nullable=True, default=0.0)
    text = Column(String(1024))
    user = relationship("User",
                        cascade="all, delete, delete-orphan",
                        backref='labs')
