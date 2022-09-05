#!/usr/bin/python3

"""
A subclass module of BaseModel
located in the base_model.py
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    A subclass module of BaseModel
    with some added attributes
    """
    place_id = ""
    user_id = ""
    text = ""
