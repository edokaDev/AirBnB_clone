#!/usr/bin/python3
"""Parent class BaseModel that defines all attributes for other classes."""

from datetime import datetime
import uuid
import models


class BaseModel:
    """Parent for all the other subclasses to follow."""

    def __init__(self, *args, **kwargs):
        """Initialize attributes when an object is made."""
        if kwargs:
            del kwargs['__class__']
            self.__dict__.update(kwargs)
            self.created_at = datetime.fromisoformat(kwargs['created_at'])
            self.updated_at = datetime.fromisoformat(kwargs['updated_at'])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return a string representantion of the object."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update updated_at attribute with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the object."""
        dictionary = self.__dict__.copy()
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.update({"__class__": self.__class__.__name__})
        return dictionary
