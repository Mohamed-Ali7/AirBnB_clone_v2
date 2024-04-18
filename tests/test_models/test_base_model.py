#!/usr/bin/python3
"""This module contains TestBaseModel class to test BaseModel class"""
import unittest
from models.base_model import BaseModel
from datetime import datetime
import os
from models import storage


class TestBaseModel(unittest.TestCase):
    """This class is for testing BaseModel class attributes and functions"""

    def test_instantiation(self):
        """Tests creating an instance of BaseModel class"""

        b1 = BaseModel()
        old_updated_at = b1.updated_at
        b1_dict = b1.to_dict()

        self.assertEqual(len(b1.id), 36)

        # Checking attributes types
        self.assertEqual(type(b1.id), str)
        self.assertEqual(type(b1.created_at), datetime)
        self.assertEqual(type(b1.updated_at), datetime)
        self.assertEqual(type(b1_dict["created_at"]), str)
        self.assertEqual(type(b1_dict["updated_at"]), str)

        self.assertLess(b1.created_at, b1.updated_at)

        # Checking __class__ attribute in __dict__ and to_dict()
        self.assertNotEqual(b1.created_at, old_updated_at)
        self.assertTrue("__class__" in b1_dict)
        self.assertTrue("__class__" not in b1.__dict__)

        # Creating a new instance using kwargs
        b2 = BaseModel(**b1_dict)

        self.assertTrue("__class__" in b2.to_dict())
        self.assertTrue("__class__" not in b2.__dict__)

        self.assertTrue(b2.to_dict()["__class__"], "BaseModel")

        # Checking datetime attributes types
        self.assertEqual(type(b2.created_at), datetime)
        self.assertEqual(type(b2.updated_at), datetime)

        # Checking if the two instances are the same object
        self.assertTrue(b1 is not b2)
        self.assertTrue(b1 != b2)

        # Checking if the two instance's attributes are equal
        self.assertEqual(b1.id, b2.id)
        self.assertEqual(b1.to_dict(), b2.to_dict())

        # Set new attribute to b2 instance
        b2.name = "BaseModel class"
        self.assertNotEqual(b1.to_dict(), b2.to_dict())
        self.assertTrue("name" in b2.to_dict())
        self.assertTrue("name" not in b1.to_dict())

        # Tests that the each new created instance has a unique id
        b3 = BaseModel()
        self.assertNotEqual(b2.id, b3.id)
        self.assertEqual(len(b3.id), 36)
        self.assertEqual(type(b1.id), str)

        self.assertLess(b1.created_at, b3.created_at)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Only runs when using the file storage")
    def test_save(self):
        """Tests (save) function"""
        b1 = BaseModel()
        old_updated_at = b1.updated_at

        self.assertFalse(os.path.exists("file.json"))

        # Tests if updated_at attribute has changed after calling save() method
        b1.save()
        self.assertNotEqual(old_updated_at, b1.updated_at)
        self.assertTrue(b1 in storage.all().values())
        self.assertTrue(os.path.exists("file.json"))

        with self.assertRaises(TypeError):
            b1.save(None)
        with self.assertRaises(TypeError):
            b1.save("None")

        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_str(self):
        """Tests __str__ function"""

        b1 = BaseModel()
        b1_str = f"[{b1.__class__.__name__}] ({b1.id}) {b1.__dict__}"
        self.assertEqual(b1.__str__(), b1_str)

        self.assertEqual(type(b1.__str__()), str)

        # Adding new attribute to change b1.__dict__
        b1.name = "BaseModel class"
        self.assertNotEqual(b1.__str__(), b1_str)

        with self.assertRaises(TypeError):
            b1.__str__(None)
        with self.assertRaises(TypeError):
            b1.__str__("None")

    def test_to_dict(self):
        """Tests to_dict function"""

        b1 = BaseModel()
        temp_dict1 = {'id': b1.id,
                      'created_at': b1.created_at.isoformat(),
                      'updated_at': b1.updated_at.isoformat(),
                      '__class__': b1.__class__.__name__}

        self.assertEqual(b1.to_dict(), temp_dict1)
        self.assertNotEqual(b1.to_dict(), b1.__dict__)

        b1.name = "BaseModel class"
        self.assertNotEqual(b1.to_dict(), temp_dict1)

        temp_dict2 = {'id': b1.id,
                      'created_at': b1.created_at.isoformat(),
                      'updated_at': b1.updated_at.isoformat(),
                      '__class__': b1.__class__.__name__,
                      "name": "BaseModel class"}

        self.assertEqual(b1.to_dict(), temp_dict2)

        # Tests that created_at and updated_at from to_dict() function
        # Matching iso format
        self.assertEqual(b1.created_at,
                         datetime.fromisoformat(temp_dict1["created_at"]))

        self.assertEqual(b1.created_at,
                         datetime.strptime(temp_dict1["created_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))

        self.assertEqual(b1.updated_at,
                         datetime.fromisoformat(temp_dict1["updated_at"]))

        self.assertEqual(b1.updated_at,
                         datetime.strptime(temp_dict1["updated_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        with self.assertRaises(TypeError):
            b1.to_dict(None)
        with self.assertRaises(TypeError):
            b1.to_dict("None")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Only runs when using the file storage")
    def test_delete_method(self):
        # Test delete method removes instance from storage
        model = BaseModel()
        model_id = model.id
        storage.new(model)
        storage.save()
        model.delete()
        self.assertNotIn(f"BaseModel.{model_id}", storage.all())
        if os.path.exists("file.json"):
            os.remove("file.json")
