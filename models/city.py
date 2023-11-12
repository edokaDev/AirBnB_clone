#!/usr/bin/python3
"""Class that defines the city the user is from."""

from models.base_model import BaseModel


class City(BaseModel):
    """Inherit other attributes from BaseModel."""

    state_id = ''
    name = ''
