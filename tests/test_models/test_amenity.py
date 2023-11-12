#!/usr/bin/python3
"""Test for the Amenity class."""

import unittest
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Test for the Amenity Class."""

    def setUp(self):
        """Sets up the object's attributes before running tests."""
        self.obj = Amenity()
        self.obj.name = 'Kyalo'

    def test_attributes(self):
        """Test the Amenity class attributes."""
        amenity = Amenity()
        self.assertEqual(amenity.name, "")
        self.assertEqual(self.obj.name, "Kyalo")

    def test_inheritance(self):
        """Test that Amenity inherits from BaseModel."""
        amenity = Amenity()
        self.assertTrue(issubclass(Amenity, BaseModel))
        self.assertTrue(isinstance(amenity, BaseModel))

    def test_to_dict(self):
        """Test the to_dict() method."""
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(amenity_dict['__class__'], 'Amenity')
        self.assertTrue('id' in amenity_dict)
        self.assertTrue('created_at' in amenity_dict)
        self.assertTrue('updated_at' in amenity_dict)

    def test_from_dict(self):
        """Test creating a Amenity instance from a dictionary."""
        amenity_data = {
            '__class__': 'Amenity',
            'id': '12345',
            'created_at': '2023-10-17T12:34:56.789012',
            'updated_at': '2023-10-17T12:34:56.789012',
        }
        amenity = Amenity(**amenity_data)
        self.assertEqual(amenity.id, '12345')
