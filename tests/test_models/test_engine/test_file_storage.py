#!/usr/bin/python3
"""Test for the FileStorage class."""

import os
import unittest
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

class TestFileStorage(unittest.TestCase):
    """Test for the FileStorage Class."""

    @classmethod
    def setUpClass(cls):
        """Set up file path for testing and clean up any existing test data."""
        cls.file_path = "test_file.json"
        if os.path.exists(cls.file_path):
            os.remove(cls.file_path)

    def test_file_storage(self):
        """Checks if file is name is given."""
        storage = FileStorage()
        try:
            storage.reload()
        except Exception as e:
            raise FileNotFoundError

    def test_all(self):
        """Checks if the all() returns an empty dictionary."""
        storage = FileStorage()
        storage.reload()
        dictionary = storage.all()
        self.assertNotEqual(dictionary, {})

    def test_new(self):
        """Checks if new() does its job."""
        obj = BaseModel()
        storage = FileStorage()
        storage.new(obj)
        dictionary = storage.all()
        self.assertNotEqual(dictionary, {})

    def test_save(self):
        """Checks if save() does its job."""
        storage = FileStorage()
        obj = BaseModel()
        obj.save()

        with open('storage_file.json', 'r', encoding='utf') as f:
            dictionary = json.load(f)

        key = '.'.join((obj.__class__.__name__, obj.id))
        if key not in dictionary.keys():
            raise KeyError

    def test_reload(self):
        """Checks if reload() does its job."""
        storage = FileStorage()
        obj = BaseModel()
        obj.save()
        storage.reload()
        dictionary = storage.all()
        key = '.'.join((obj.__class__.__name__, obj.id))

        if key not in dictionary:
            raise KeyError

    def test_file_storage_new_and_all(self):
        """Test the new and all methods of FileStorage."""
        storage = FileStorage()
        model = BaseModel()
        storage.new(model)
        all_objects = storage.all()
        self.assertTrue(isinstance(all_objects, dict))
        self.assertIn(f"BaseModel.{model.id}", all_objects)

    def test_file_storage_save_and_reload(self):
        """Test the save and reload methods of FileStorage."""
        storage = FileStorage()
        model = BaseModel()
        storage.new(model)
        storage.save()

        # Create a new storage instance and reload the data
        new_storage = FileStorage()
        new_storage.reload()
        all_objects = new_storage.all()
        self.assertIn(f"BaseModel.{model.id}", all_objects)

    @classmethod
    def tearDownClass(cls):
        """Clean up test file after tests are done."""
        if os.path.exists(cls.file_path):
            os.remove(cls.file_path)
