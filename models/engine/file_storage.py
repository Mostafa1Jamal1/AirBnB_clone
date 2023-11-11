#!/usr/bin/python3
"""Storage engine to serializes instances to a JSON
file and deserializes JSON file to instances"""


import models.base_model.BaseModel as BaseModel
import json
from os.path import exists


class FileStorage:
    """
    Handles the serialization and deserialization of
    instances to and from a JSON file.

    Private class attributes:
        __file_path: string - path to the JSON file (ex: file.json)
        __objects: dictionary - empty but will store
        all objects by <class name>.id
                     (ex: to store a BaseModel object
                     with id=12121212, the key will be BaseModel.12121212)

    Public instance methods:
        all(self): returns the dictionary __objects
        new(self, obj): sets in __objects the
        obj with key <obj class name>.id
        save(self): serializes __objects to the
        JSON file (path: __file_path)
        reload(self): deserializes the JSON file to
        __objects (only if the JSON file (__file_path) exists;
                      otherwise, do nothing. If the file doesn’t
                      exist, no exception should be raised)
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Adds a new object to __objects with the key <obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        data = {}
        for key, obj in self.__objects.items():
            data[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the
        JSON file (__file_path) exists).
        If the file doesn’t exist, no exception should be raised.
        """
        if exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file.read())

            for key, value in data.items():
                class_name, obj_id = key.split('.')
                class_ = globals()[class_name]
                obj = class_(**value)
                self.__objects[key] = obj
