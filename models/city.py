"""Class that defines the city the user is from."""
from models.base_model import BaseModel


class City(BaseModel):
    """Inherits other attributes from BaseModel."""
    state_id = ''
    name = ''
