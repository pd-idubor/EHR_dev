#!/usr/bin/python3
"""
    Defines the 'User' class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.complaint import Complaint
from hashlib import md5


plan = Table("plan", Base.metadata,
             Column('user_id', String(60),
                    ForeignKey('user.id'), primary_key=True),
             Column('medics_id', String(60),
                    ForeignKey('medics.id'), primary_key=True),
             Column('procedure_id', String(60),
                    ForeignKey('procedures.id'), primary_key=True))


class User(BaseModel, Base):
    """
        User class
    """
    __tablename__ = "user"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    demo_id = Column(String(60), ForeignKey("demo.id"), nullable=True)
    labs_id = Column(String(60), ForeignKey("labs.id"), nullable=True)
    practitioner_id = Column(String(60),
                             ForeignKey("practitioner.id"), nullable=True)
    medics = relationship("Medics",
                          secondary="plan", viewonly=False)
    procedure  = relationship("Procedure",
                              secondary="plan", viewonly=True)

    complaint = relationship("Complaint",
                             cascade="all", backref="user")
    history = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Store password with md5 value"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
