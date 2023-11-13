"""Contains Unittests for Base_model class."""
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Different methods with different cases."""

    def setUp(self):
        """Sets up the object before running the methods."""
        self.obj = BaseModel()
        self.obj.name = "Brian"
        self.obj.number = 1

    def test_basic_initialization(self):
        """Checks when object is made directly."""
        self.assertAlmostEqual(self.obj.name, "Brian")
        self.assertAlmostEqual(self.obj.number, 1)

    def test_str(self):
        """Checks the __str__ method."""
        class_name = self.obj.__class__.__name__
        string = f"[{class_name}] ({self.obj.id}) {self.obj.__dict__}"
        self.assertEqual(self.obj.__str__(), string)

    def test_to_dict(self):
        """Tests the to_dict method."""
        dictionary = self.obj.__dict__.copy()
        dictionary['created_at'] = self.obj.created_at.isoformat()
        dictionary['updated_at'] = self.obj.updated_at.isoformat()
        dictionary.update({'__class__': 'BaseModel'})
        self.assertAlmostEqual(self.obj.to_dict(), dictionary)

    def test_dict_obj(self):
        """Tests an object made using kwargs."""
        kwargs = self.obj.to_dict()
        new_obj = BaseModel(**kwargs)
        self.assertEqual(self.obj.id, new_obj.id)
        self.assertEqual(self.obj.name, new_obj.name)
        self.assertEqual(self.obj.created_at, new_obj.created_at)
        self.assertEqual(self.obj.updated_at, new_obj.updated_at)
        self.assertEqual(self.obj.number, new_obj.number)
        
    def test_created_at(self):
        """Checks if created_at attribute is the right type."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_save(self):
        "Tests the save method"
        self.obj.name = "Edoka"
        print(self.obj.created_at)
        self.obj.save()
        self.obj.save()
        self.obj.save()
        print(self.obj.created_at)
        self.assertNotEqual(self.obj.updated_at, self.obj.created_at)
        self.assertEqual(self.obj.name, "Edoka")


if __name__ == "__main__":
    unittest.main()
