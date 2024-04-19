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

    def test_todict(self):
        """Tests to_dict method"""

        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        # Tests if it's a dictionary
        self.assertIsInstance(self.value().to_dict(), dict)
        # Tests if to_dict contains accurate keys
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        # Tests if to_dict contains added attributes
        mdl = self.value()
        mdl.firstname = 'Celestine'
        mdl.lastname = 'Akpanoko'
        self.assertIn('firstname', mdl.to_dict())
        self.assertIn('lastname', mdl.to_dict())
        # Tests to_dict datetime attributes if they are strings
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        # Tests to_dict output
        datetime_now = datetime.today()
        mdl = self.value()
        mdl.id = '012345'
        mdl.created_at = mdl.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': mdl.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(mdl.to_dict(), to_dict)
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
                self.value(id='u-b34').to_dict(),
                {
                    '__class__': mdl.__class__.__name__,
                    'id': 'u-b34'
                }
            )

        # Tests to_dict output contradiction
        mdl_d = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(mdl_d.to_dict(), mdl_d.__dict__)
        self.assertNotEqual(
            mdl_d.to_dict()['__class__'],
            mdl_d.__class__
        )
        # Tests to_dict with arg
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(45)
        self.assertNotIn('_sa_instance_state', n)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Only runs when using the file storage")
    def test_delete_method(self):
        # Test delete method removes instance from storage
        model = self.value()
        model_id = model.id
        model.save()
        model.delete()
        self.assertNotIn(f"BaseModel.{model_id}", storage.all())
