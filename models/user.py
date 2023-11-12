#!/usr/bin/python3
"""Used to represent a user."""

from models.base_model import BaseModel


class User(BaseModel):
    """Contain attributes that define the user."""

    email = ''
    password = ''
    first_name = ''
    last_name = ''
