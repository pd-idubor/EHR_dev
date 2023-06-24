#!/usr/bin/python3
"""
    Initialize package
"""
from os import getenv
from models.engine.storage import Storage

storage = Storage()
storage.reload()
