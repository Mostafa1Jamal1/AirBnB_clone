#!/usr/bin/python3
"""unittest cases for the base model class"""


import unittest
from models.base_model import BaseModel
from datetime import datetime
import time


class TestBaseModel(unittest.TestCase):
    """To consider all the possible test cases"""

    def test_id_is_string(self):
        """
        Test that the 'id' attribute is a string.
        """
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)

    def test_id_uniqueness(self):
        """
        Test the uniqueness of the 'id' attribute.
        """
        instances = [BaseModel() for _ in range(5)]
        id_set = set(instance.id for instance in instances)
        self.assertEqual(len(id_set), len(instances))

    def test_creat_at_update_at_datetime_objects(self):
        """
        Test that 'created_at' and 'updated_at'
        are instances of datetime.
        """
        obj = BaseModel()
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_created_at_and_updated_at_initial(self):
        """
        Test that 'created_at' and 'updated_at' are
        set to the current datetime upon creation.
        """
        current_time = datetime.now()
        obj = BaseModel()

        time_difference_created = current_time - obj.created_at
        time_difference_updated = current_time - obj.updated_at

        self.assertLessEqual(time_difference_created.total_seconds(), 1)
        self.assertLessEqual(time_difference_updated.total_seconds(), 1)

    def test_updated_at_created_at_when_save_is_called(self):
        """
        Test that 'updated_at' is updated when
        'save' is called, but 'created_at' remains the same.
        """
        obj = BaseModel()
        initial_updated_at = obj.updated_at
        initial_created_at = obj.created_at

        time.sleep(1)

        obj.save()

        self.assertNotEqual(obj.updated_at, initial_updated_at)
        self.assertEqual(obj.created_at, initial_created_at)

        time.sleep(1)

        obj.save()

        time.sleep(1)

        obj.save()

        self.assertNotEqual(obj.updated_at, initial_updated_at)

    def test_to_dict_structure(self):
        """
        Test the structure of the returned
        dictionary when calling 'to_dict'.
        """
        obj = BaseModel()
        obj_dict = obj.to_dict()

        self.assertIsInstance(obj_dict, dict)
        self.assertIn('__class__', obj_dict)
        self.assertIn('id', obj_dict)
        self.assertIn('created_at', obj_dict)
        self.assertIn('updated_at', obj_dict)

    def test_id_in_dict_matches_instance_id(self):
        """
        Test that 'id' in the dictionary
        matches the 'id' attribute of the instance.
        """
        obj = BaseModel()
        obj_dict = obj.to_dict()

        self.assertEqual(obj_dict['id'], obj.id)

    def test_created_at_update_at_iso_format(self):
        """
        Test that 'created_at' and 'updated_at'
        in the dictionary are in ISO format.
        """
        obj = BaseModel()
        obj_dic = obj.to_dict()

        iso = "%Y-%m-%dT%H:%M:%S.%f"
        create_dic = datetime.strptime(obj_dic['created_at'], iso)
        self.assertEqual(create_dic, obj.created_at)

    def test_class_in_dict_matches_instance_class(self):
        """
        Test that '__class__' in the dictionary
        matches the class name of the instance.
        """
        obj = BaseModel()
        obj_dict = obj.to_dict()
        self.assertEqual(obj_dict['__class__'], 'BaseModel')

    def test_only_instance_attributes_in_dict(self):
        """
        Test that only instance attributes
        are included in the dictionary.
        """
        custom_attribute = "Custom Value"
        obj = BaseModel()
        obj.custom_attribute = custom_attribute
        obj_dict = obj.to_dict()

        self.assertIn('custom_attribute', obj_dict)

    def test_default_str_output(self):
        """
        Test the default __str__ output of the BaseModel class.
        """
        obj = BaseModel()
        str_output = str(obj)
        expected_output = f"[BaseModel] ({obj.id}) {obj.__dict__}"

        self.assertEqual(str_output, expected_output)

    def test_create_instance_from_dict(self):
        """
        Test creating a BaseModel instance from a
        dictionary representation.
        """
        my_obj = BaseModel()
        obj_dict = my_obj.to_dict()

        obj = BaseModel(**obj_dict)

        self.assertEqual(obj.__class__.__name__, obj_dict['__class__'])
        self.assertEqual(obj.created_at.isoformat(), obj_dict['created_at'])
        self.assertEqual(obj.updated_at.isoformat(), obj_dict['updated_at'])


if __name__ == '__main__':
    unittest.main()
