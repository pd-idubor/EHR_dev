#!/usr/bin/python3
"""Defines common attributes and methods for other classes"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv

Base = declarative_base()


class BaseModel():
    """Parent class"""
    
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialization"""
        
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        #Recreate an instance from dict representation
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        if (len(kwargs) != 0):
            for k, v in kwargs.items():
                if (k == 'created_at' or k == 'updated_at'):
                    self.__dict__[k] = datetime.strptime(v, t_format)
                else:
                    if (k != '__class__'):
                        self.__dict__[k] = v

    def __str__(self):
        """String rep"""
        dct = self.__dict__.copy()
        dct.pop("_sa_instance_state", None)
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                self.id, dct))

    def save(self):
        """Update 'updated_at' atrribute"""
        self.updated_at = datetime.today()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, s_pass=False):
        """Return dictionary of key/value pairs"""
        
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        
        in_dct = dict(self.__dict__)
        if not s_pass and "password" in new_dict:
            del new_dict["password"]
        try:
            del in_dct['_sa_instance_state']

        except KeyError:
            pass

        in_dct['__class__'] = self.__class__.__name__
        in_dct['created_at'] = self.created_at.strftime(t_format)
        in_dct['updated_at'] = self.updated_at.strftime(t_format)

        return (in_dct)
    def delete(self):
        """Delete"""
        models.storage.delete(self)
