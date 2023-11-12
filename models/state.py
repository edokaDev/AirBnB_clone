#!/usr/bin/python3
"""Class that defines which state the user is from."""
from models.base_model import BaseModel


class State(BaseModel):
    """Inherits other attributes from BaseModel."""
    name = ''
    