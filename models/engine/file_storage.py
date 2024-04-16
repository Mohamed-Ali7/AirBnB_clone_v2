#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            cls_objects = {
                key: value for key, value in FileStorage.__objects.items()
                if cls.__name__ in key
                }

            return cls_objects

        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        (ex: to store a BaseModel object with id=12121212,
        the key will be BaseModel.12121212)

        Args:
        obj (dict): Is the dict representaion of the object to add to
        (__objects) dictionary
        """

        obj_key = f"{obj.__class__.__name__}.{obj.id}"

        FileStorage.__objects[obj_key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""

        with open(FileStorage.__file_path, "w") as file:
            serialized_objects = {}
            for key, value in FileStorage.__objects.items():
                serialized_objects[key] = value.to_dict()
            json.dump(serialized_objects, file, indent=4)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists, otherwise, do nothing.
        If the file doesn’t exist, no exception should be raised)
        """

        try:
            with open(FileStorage.__file_path, "r") as file:
                deserialized_objects = json.load(file)
                for key, value in deserialized_objects.items():
                    obj = eval(value["__class__"])(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside"""

        if obj is None:
            return

        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        del FileStorage.__objects[obj_key]
