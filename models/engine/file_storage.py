#!/usr/bin/python3
"""Serializes and deserializes instances to and from a JSON file."""
from datetime import datetime
import json
import os
from . import (
    BaseModel,
    User,
    Amenity,
    City,
    Place,
    Review,
    State
)


class FileStorage:
    """Will be used for storing and retrieving objects.

    __objects: is a dictionary of all the created objects
    __file_path: is the path to the json file where the serialized
    dictonary is stored.
    """

    __file_path = 'storage_file.json'
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set the key of the obj for the __objects dictionary.

        The format used is class_name.id.
        """
        class_name = '.'.join((type(obj).__name__, obj.id))

        # we save the object directly into the objects dictionary,
        # not as a dictionary, but as an instance of its class
        # this way, when the object it call, it is seen as an instance
        # of its class and so, the __str__ function can be accessed.
        FileStorage.__objects.update({class_name: obj})

    def save(self):
        """Serialize inject to json string.

        and saves them to the __file_path.
        """
        save = {}
        for obj in FileStorage.__objects:
            save[obj] = FileStorage.__objects[obj].to_dict()

        # json_string = json.dumps(FileStorage.__objects)
        json_string = json.dumps(save)

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            f.write(json_string)

    def reload(self):
        """Deserialize a json file and stores the dict in __objects."""
        # check if the file path exist, else do nothing
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as file:
                # load the file into a json object
                objs = dict(json.load(file))

                for obj in objs:
                    obj_key = obj.split('.')
                    # get the class name
                    model_class = obj_key[0]
                    instance = objs[obj].copy()

                    # update the time stamps to datetime format
                    instance['created_at'] = str(
                        datetime.strptime(
                            instance['created_at'],
                            "%Y-%m-%dT%H:%M:%S.%f"
                        )
                    )
                    instance['updated_at'] = str(
                        datetime.strptime(
                            instance['updated_at'],
                            "%Y-%m-%dT%H:%M:%S.%f"
                        )
                    )
                    instance = globals()[model_class](**instance)
                    FileStorage.__objects[obj] = instance
