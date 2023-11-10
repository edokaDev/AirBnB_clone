"""Serializes instances to a JSON file and deserializes JSON file to instances."""
import json
from models.base_model import BaseModel


class FileStorage:
    """Will be used for storing and retrieving objects.
    __objects: is a dictionary of all the created objects
    __file_path: is the path to the json file where the serialized
    dictonary is stored.
    """
    __file_path = 'storage_file.json'
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets the key of the obj for the __objects dictionary.
        The format used is class_name.id
        """
        class_name = type(obj).__name__ + '.' + obj.id
        obj_dict = obj.to_dict()
        #if class_name in FileStorage.__objects.keys():
            #FileStorage.__objects[class_name] = obj_dict
        #else:
        FileStorage.__objects.update({class_name: obj_dict}) #adds the new object to dictonary

    def save(self):
        """Serializes inject to json string and saves them
        to the __file_path.
        """
        json_string = json.dumps(FileStorage.__objects)

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            f.write(json_string)

    def reload(self):
        """Deserializes a json file and stores the dictionary
        in __objects.
        """
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                FileStorage.__objects = json.load(f)

        except Exception:
            return
