#!/usr/bin/python3
"""This module contains TestBaseModel class to test BaseModel class"""
import json
import unittest
from models.base_model import BaseModel
from datetime import datetime
import os
from models import storage


class TestBaseModel(unittest.TestCase):
    """This class is for testing BaseModel class attributes and functions"""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Executes before each test method"""
        pass

    def tearDown(self):
        """Executes after each test method"""
        if os.path.exists("file.json"):
            os.remove('file.json')

    def test_default(self):
        """Tests normal initialization"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Tests initialization through kwargs"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Tests raising exception when kwargs is an int"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_kwargs_none(self):
        """Tests when kwargs is none"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """Tests when there is only one kwargs provided"""
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """Tests id"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Tests created_at attribute"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """Tests updated_at attribute"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Only runs when using the file storage")
    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

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

        b1 = self.value()
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
        self.assertNotIn('_sa_instance_state', temp_dict1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Only runs when using the file storage")
    def test_delete_method(self):
        # Test delete method removes instance from storage
        model = self.value()
        model_id = model.id
        model.save()
        model.delete()
        self.assertNotIn(f"BaseModel.{model_id}", storage.all())
