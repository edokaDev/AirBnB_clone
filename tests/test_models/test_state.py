#!/usr/bin/python3
"""Tests for state class."""
import unittest
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Tests for State's attributes."""

    def setUp(self):
        "Sets up attributes before test methods"
        self.obj = State()
        self.obj.name = 'Texas'

    def test_inheritance(self):
        """Test that State inherits from BaseModel."""
        self.assertTrue(issubclass(State, BaseModel))
        self.assertTrue(isinstance(self.obj, BaseModel))

    def test_to_dict(self):
        """Test the to_dict() method."""
        state_dict = self.obj.to_dict()
        self.assertEqual(state_dict['__class__'], 'State')
        self.assertTrue('id' in state_dict)
        self.assertTrue('created_at' in state_dict)
        self.assertTrue('updated_at' in state_dict)

    def test_from_dict(self):
        """Test creating a Test instance from a dictionary."""
        state_data = {
            '__class__': 'State',
            'id': '12345',
            'created_at': '2023-10-17T12:34:56.789012',
            'updated_at': '2023-10-17T12:34:56.789012',
        }
        state = State(**state_data)
        self.assertEqual(state.id, '12345')
        print(state.created_at)

    def test_obj_name(self):
        """Checks if the name initialized successfuly."""
        self.assertEqual(self.obj.name, 'Texas')

    def test_dict_obj(self):
        """Tests an object made using kwargs."""
        kwargs = self.obj.to_dict()
        new_obj = State(**kwargs)
        self.assertEqual(self.obj.id, new_obj.id)
        self.assertEqual(self.obj.name, new_obj.name)
        self.assertEqual(self.obj.created_at, new_obj.created_at)
        self.assertEqual(self.obj.updated_at, new_obj.updated_at)
        self.assertEqual(self.obj.name, new_obj.name)
