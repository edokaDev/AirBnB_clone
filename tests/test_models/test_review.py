#!/usr/bin/python3
"""Test for the Review class."""

import unittest
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Test for the Review Class."""

    def setUp(self):
        """Sets up the object's attributes before running tests."""
        self.obj = Review()
        self.obj.place_id = '.'.join(('Place', self.obj.id))
        self.obj.user_id = '.'.join(('User', self.obj.id))
        self.obj.text = 'Enjoy your stay'

    def test_attributes(self):
        """Test the Review class attributes."""
        review = Review()
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(self.obj.place_id, '.'.join(('Place', self.obj.id)))
        self.assertEqual(self.obj.user_id, '.'.join(('User', self.obj.id)))
        self.assertEqual(self.obj.text, 'Enjoy your stay')

    def test_inheritance(self):
        """Test that Review inherits from BaseModel."""
        review = Review()
        self.assertTrue(issubclass(Review, BaseModel))
        self.assertTrue(isinstance(review, BaseModel))

    def test_to_dict(self):
        """Test the to_dict() method."""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(review_dict['__class__'], 'Review')
        self.assertTrue('id' in review_dict)
        self.assertTrue('created_at' in review_dict)
        self.assertTrue('updated_at' in review_dict)

    def test_from_dict(self):
        """Test creating a Review instance from a dictionary."""
        review_data = {
            '__class__': 'Review',
            'id': '12345',
            'created_at': '2023-10-17T12:34:56.789012',
            'updated_at': '2023-10-17T12:34:56.789012',
            'place_id' : 'Place.12345',
            'user_id' : 'User.12345',
            'text' : 'Enjoy your stay'
        }
        review = Review(**review_data)
        self.assertEqual(review.id, '12345')
        self.assertEqual(review.place_id, 'Place.12345')
        self.assertEqual(review.user_id, 'User.12345')
        self.assertEqual(review.text, 'Enjoy your stay')
