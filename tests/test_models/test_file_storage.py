#!/usr/bin/python3
"""Test for the FileStorage class."""

import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os


class TestFileStorage(unittest.TestCase):
    """Test for the FileStorage Class."""

    @classmethod
    def setUpClass(cls):
        """Set up file path for testing and clean up any existing test data."""
        cls.file_path = "test_file.json"
        if os.path.exists(cls.file_path):
            os.remove(cls.file_path)

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

        #Create a new storage instance and reload the data
        new_storage = FileStorage()
        new_storage.reload()
        all_objects = new_storage.all()
        self.assertIn(f"BaseModel.{model.id}", all_objects)

    @classmethod
    def tearDownClass(cls):
        """Clean up test file after tests are done."""
        if os.path.exists(cls.file_path):
            os.remove(cls.file_path)
