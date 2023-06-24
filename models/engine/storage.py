#!/usr/bin/python3
"""Describes DBStorage class"""
import models
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base, BaseModel
from models.user import User
from models.labs import Labs
from models.demo import Demo
from models.complaint import Complaint
from models.medics import Medics
from models.procedure import Procedure
from models.diagnosis import Diagnosis
from models.practitioner import Practitioner


classes = {"BaseModel": BaseModel, "User": User, "Demo": Demo,
            "Complaint": Complaint,
            "Diagnosis": Diagnosis, "Labs": Labs,
            "Medics": Medics, "Procedure": Procedure,
            "Practitioner": Practitioner
            }

class Storage():
    """Database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization"""

        connect = "mysql+mysqldb://{}:{}@{}/{}"
        db = getenv('EHR_MYSQL_DB', default=None)
        username = getenv('EHR_MYSQL_USER', default=None)
        passwd = getenv('EHR_MYSQL_PWD', default=None)
        host = getenv('EHR_MYSQL_HOST', default=None)

        self.__engine = create_engine(
                connect.format(username, passwd, host, db), pool_pre_ping=True)

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from current session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)

        self.__session = Session()

    def close(self):
        """Closes a session"""
        self.__session.close()

    def get(self, cls, id):
        """Retrieves one object based on class name and id"""
        if cls and id:
            all_objs = models.storage.all(cls)
            for value in all_objs.values():
                if (value.id == id):
                    return value
        return None

    def count(self, cls=None):
        """Count the number of objects in storage"""
        return len(self.all(cls))
