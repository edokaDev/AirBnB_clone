#!/usr/bin/python3
"""Runs unittests for Place class."""
import unittest
from models.base_model import BaseModel
from models.place import Place


class TestPlace(unittest.TestCase):
    """Tests if attributes are initialized correctly."""
    def setUp(self):
        "Sets up attributes before test methods"
        self.obj = Place()
        self.obj.city_id = '.'.join(('City', self.obj.id))
        self.obj.user_id = '.'.join(('User', self.obj.id))
        self.obj.name = 'Brian'
        self.obj.description = 'Best Hotel in the city'
        self.obj.number_rooms = 20
        self.obj.number_bathrooms = 20
        self.obj.max_guest = 20
        self.obj.price_by_night = 500
        self.obj.latitude = 60.0
        self.obj.longitude = 30.0
        self.obj.amenity_ids = ["Swimming Pool", "Sauna"]

    def test_inheritance(self):
        """Test that Place inherits from BaseModel."""
        self.assertTrue(issubclass(Place, BaseModel))
        self.assertTrue(isinstance(self.obj, BaseModel))

    def test_to_dict(self):
        """Test the to_dict() method."""
        place_dict = self.obj.to_dict()
        self.assertEqual(place_dict['__class__'], 'Place')
        self.assertTrue('id' in place_dict)
        self.assertTrue('created_at' in place_dict)
        self.assertTrue('updated_at' in place_dict)

    def test_from_dict(self):
        """Test creating a Place instance from a dictionary."""
        place_data = {
            '__class__': 'Place',
            'id': '12345',
            'created_at': '2023-10-17T12:34:56.789012',
            'updated_at': '2023-10-17T12:34:56.789012',
        }
        place = Place(**place_data)
        self.assertEqual(place.id, '12345')
        print(place.created_at)

    def test_obj_name(self):
        """Checks if the name initialized successfuly."""
        self.assertEqual(self.obj.name, 'Brian')
        self.assertEqual(self.obj.city_id, '.'.join(('City', self.obj.id)))

    def test_dict_obj(self):
        """Tests an object made using kwargs."""
        kwargs = self.obj.to_dict()
        new_obj = Place(**kwargs)
        self.assertEqual(self.obj.id, new_obj.id)
        self.assertEqual(self.obj.name, new_obj.name)
        self.assertEqual(self.obj.created_at, new_obj.created_at)
        self.assertEqual(self.obj.updated_at, new_obj.updated_at)
        self.assertEqual(self.obj.name, new_obj.name)
        self.assertEqual(self.obj.city_id, new_obj.city_id)
        self.assertEqual(self.obj.user_id, new_obj.user_id)
        self.assertEqual(self.obj.description, new_obj.description)
        self.assertEqual(self.obj.number_rooms, new_obj.number_rooms)
        self.assertEqual(self.obj.number_bathrooms, new_obj.number_bathrooms)
        self.assertEqual(self.obj.max_guest, new_obj.max_guest)
        self.assertEqual(self.obj.price_by_night, new_obj.price_by_night)
        self.assertEqual(self.obj.longitude, new_obj.longitude)
        self.assertEqual(self.obj.latitude, new_obj.latitude)
        self.assertEqual(self.obj.amenity_ids, new_obj.amenity_ids)
