#!/usr/bin/python3

"""
A submodule of base_model.py
"""
from models import base_model


class User(base_model.BaseModel):
    """
    A subclass of BaseModel Class
    with some added attributes
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
