#!/usr/bin/python3
"""This module contains TestAmenity class to test Amenity class"""
import unittest
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from datetime import datetime
import os


class TestAmenity(unittest.TestCase):
    """This class is for testing Amenity class attributes and functions"""

    def test_instantiation(self):
        """Tests creating an instance of Amenity class"""

        a1 = Amenity()
        old_updated_at = a1.updated_at
        a1_dict = a1.to_dict()

        self.assertEqual(len(a1.id), 36)
        self.assertTrue(isinstance(a1, BaseModel))

        # Checking attributes types
        self.assertEqual(type(a1.id), str)
        self.assertEqual(type(a1.created_at), datetime)
        self.assertEqual(type(a1.updated_at), datetime)
        self.assertEqual(type(a1_dict["created_at"]), str)
        self.assertEqual(type(a1_dict["updated_at"]), str)

        self.assertLess(a1.created_at, a1.updated_at)

        # Checking __class__ attribute in __dict__ and to_dict()
        self.assertNotEqual(a1.created_at, old_updated_at)
        self.assertTrue("__class__" in a1_dict)
        self.assertTrue("__class__" not in a1.__dict__)

        # Creating a new instance using kwargs
        a2 = Amenity(**a1_dict)

        self.assertTrue("__class__" in a2.to_dict())
        self.assertTrue("__class__" not in a2.__dict__)

        self.assertTrue(a2.to_dict()["__class__"], "BaseModel")

        # Checking datetime attributes types
        self.assertEqual(type(a2.created_at), datetime)
        self.assertEqual(type(a2.updated_at), datetime)

        # Checking if the two instances are the same object
        self.assertTrue(a1 is not a2)
        self.assertTrue(a1 != a2)

        # Checking if the two instance's attributes are equal
        self.assertEqual(a1.id, a2.id)
        self.assertEqual(a1.to_dict(), a2.to_dict())

        # Set new attribute to a2 instance
        a2.zip_code = "Amenity 0xa7"
        self.assertNotEqual(a1.to_dict(), a2.to_dict())
        self.assertTrue("zip_code" in a2.to_dict())
        self.assertTrue("zip_code" not in a1.to_dict())

        # Tests that the each new created instance has a unique id
        a3 = Amenity()
        self.assertNotEqual(a2.id, a3.id)
        self.assertEqual(len(a3.id), 36)

        self.assertLess(a1.created_at, a3.created_at)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'Only run this test when the storage is a file')
    def test_save_with_file(self):
        """Tests (save) function"""
        a1 = Amenity()
        old_updated_at = a1.updated_at

        self.assertTrue(not os.path.exists("file.json"))

        # Tests if updated_at attribute has changed after calling save() method
        a1.save()
        self.assertNotEqual(old_updated_at, a1.updated_at)
        self.assertIn(f"{a1.__class__.__name__}.{a1.id}", storage.all())

        self.assertTrue(os.path.exists("file.json"))

        with self.assertRaises(TypeError):
            a1.save(None)
        with self.assertRaises(TypeError):
            a1.save("None")
        with self.assertRaises(TypeError):
            a1.save(Amenity())

        if os.path.exists("file.json"):
            os.remove("file.json")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db'
                     or not storage._DBStorage__engine.table_names(),
                     'Only run this test when the storage is a database')
    def test_save_with_db(self):
        # Test save method updates updated_at attribute
        amenity = Amenity(name="Parking")
        original_updated_at = amenity.updated_at

        amenity.save()
        self.assertNotEqual(original_updated_at, amenity.updated_at)
        self.assertIn(f"Amenity.{amenity.id}", storage.all())

    def test_str(self):
        """Tests __str__ function"""

        a1 = Amenity()
        a1_str = f"[{a1.__class__.__name__}] ({a1.id}) {a1.__dict__}"
        self.assertEqual(a1.__str__(), a1_str)

        self.assertEqual(type(a1.__str__()), str)

        # Adding new attribute to change a1.__dict__
        a1.name = "Amenity class"
        self.assertNotEqual(a1.__str__(), a1_str)

        with self.assertRaises(TypeError):
            a1.__str__(None)
        with self.assertRaises(TypeError):
            a1.__str__("None")

    def test_to_dict(self):
        """Tests to_dict function"""

        a1 = Amenity()

        self.assertIn("name", Amenity.__dict__.keys())

        self.assertNotIn("name", a1.to_dict())

        temp_dict1 = {'id': a1.id,
                      'created_at': a1.created_at.isoformat(),
                      'updated_at': a1.updated_at.isoformat(),
                      '__class__': a1.__class__.__name__
                      }

        self.assertEqual(a1.to_dict(), temp_dict1)
        self.assertNotEqual(a1.to_dict(), a1.__dict__)

        a1.name = "BaseModel class"
        self.assertNotEqual(a1.to_dict(), temp_dict1)

        temp_dict2 = {'id': a1.id,
                      'created_at': a1.created_at.isoformat(),
                      'updated_at': a1.updated_at.isoformat(),
                      '__class__': a1.__class__.__name__,
                      "name": "BaseModel class"}

        self.assertEqual(a1.to_dict(), temp_dict2)

        a1.name = "Test Man"
        self.assertIn("name", a1.to_dict())

        # Tests that created_at and updated_at from to_dict() function
        # Matching iso format
        self.assertEqual(a1.created_at,
                         datetime.fromisoformat(temp_dict1["created_at"]))

        self.assertEqual(a1.created_at,
                         datetime.strptime(temp_dict1["created_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))

        self.assertEqual(a1.updated_at,
                         datetime.fromisoformat(temp_dict1["updated_at"]))

        self.assertEqual(a1.updated_at,
                         datetime.strptime(temp_dict1["updated_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        with self.assertRaises(TypeError):
            a1.to_dict(None)
        with self.assertRaises(TypeError):
            a1.to_dict("None")

    def test_delete_method(self):
        """Test delete method removes instance from storage"""
        amenity = Amenity(name="Sauna")
        amenity_id = amenity.id

        storage.new(amenity)
        storage.save()
        amenity.delete()
        self.assertNotIn(f"Amenity.{amenity_id}", storage.all())

        if os.path.exists("file.json"):
            os.remove("file.json")
