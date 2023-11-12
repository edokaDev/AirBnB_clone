#!/usr/bin/python3
"""Runs unittests for City class."""
import unittest
from models.base_model import BaseModel
from models.city import City


class TestCity(unittest.TestCase):
    """Tests if attributes are initialized correctly."""
    def setUp(self):
        "Sets up attributes before test methods"
        self.obj = City()
        self.obj.name = 'Nairobi'
        self.obj.city_id = '.'.join(('City', self.obj.id))

    def test_inheritance(self):
        """Test that City inherits from BaseModel."""
        self.assertTrue(issubclass(City, BaseModel))
        self.assertTrue(isinstance(self.obj, BaseModel))

    def test_to_dict(self):
        """Test the to_dict() method."""
        city_dict = self.obj.to_dict()
        self.assertEqual(city_dict['__class__'], 'City')
        self.assertTrue('id' in city_dict)
        self.assertTrue('created_at' in city_dict)
        self.assertTrue('updated_at' in city_dict)

    def test_from_dict(self):
        """Test creating a City instance from a dictionary."""
        city_data = {
            '__class__': 'City',
            'id': '12345',
            'created_at': '2023-10-17T12:34:56.789012',
            'updated_at': '2023-10-17T12:34:56.789012',
        }
        city = City(**city_data)
        self.assertEqual(city.id, '12345')
        print(city.created_at)

    def test_obj_name(self):
        """Checks if the name initialized successfuly."""
        city_id = '.'.join(('City', self.obj.id))
        self.assertEqual(self.obj.name, 'Nairobi')
        self.assertEqual(self.obj.city_id, city_id)

    def test_dict_obj(self):
        """Tests an object made using kwargs."""
        kwargs = self.obj.to_dict()
        new_obj = City(**kwargs)
        self.assertEqual(self.obj.id, new_obj.id)
        self.assertEqual(self.obj.name, new_obj.name)
        self.assertEqual(self.obj.created_at, new_obj.created_at)
        self.assertEqual(self.obj.updated_at, new_obj.updated_at)
        self.assertEqual(self.obj.name, new_obj.name)
        self.assertEqual(self.obj.state_id, new_obj.state_id)
