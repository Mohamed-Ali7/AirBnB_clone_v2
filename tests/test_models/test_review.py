#!/usr/bin/python3
"""This module contains TestReview class to test Review class"""
import unittest
from models.place import Place
from models.state import State
from models.user import User
from models.city import City
from models.review import Review
from models.base_model import BaseModel
from datetime import datetime
import os
from models import storage


class TestReview(unittest.TestCase):
    """This class is for testing Review class attributes and functions"""

    def test_instantiation(self):
        """Tests creating an instance of Review class"""

        r1 = Review()
        old_updated_at = r1.updated_at
        r1_dict = r1.to_dict()

        self.assertEqual(len(r1.id), 36)
        self.assertTrue(isinstance(r1, BaseModel))

        # Checking attributes types
        self.assertEqual(type(r1.id), str)
        self.assertEqual(type(r1.created_at), datetime)
        self.assertEqual(type(r1.updated_at), datetime)
        self.assertEqual(type(r1_dict["created_at"]), str)
        self.assertEqual(type(r1_dict["updated_at"]), str)

        self.assertLess(r1.created_at, r1.updated_at)

        # Checking __class__ attribute in __dict__ and to_dict()
        self.assertNotEqual(r1.created_at, old_updated_at)
        self.assertTrue("__class__" in r1_dict)
        self.assertTrue("__class__" not in r1.__dict__)

        # Creating a new instance using kwargs
        r2 = Review(**r1_dict)

        self.assertTrue("__class__" in r2.to_dict())
        self.assertTrue("__class__" not in r2.__dict__)

        self.assertTrue(r2.to_dict()["__class__"], "BaseModel")

        # Checking datetime attributes types
        self.assertEqual(type(r2.created_at), datetime)
        self.assertEqual(type(r2.updated_at), datetime)

        # Checking if the two instances are the same object
        self.assertTrue(r1 is not r2)
        self.assertTrue(r1 != r2)

        # Checking if the two instance's attributes are equal
        self.assertEqual(r1.id, r2.id)
        self.assertEqual(r1.to_dict(), r2.to_dict())

        # Set new attribute to r2 instance
        r2.zip_code = "Review 0xa7"
        self.assertNotEqual(r1.to_dict(), r2.to_dict())
        self.assertTrue("zip_code" in r2.to_dict())
        self.assertTrue("zip_code" not in r1.to_dict())

        # Tests that the each new created instance has a unique id
        r3 = Review()
        self.assertNotEqual(r2.id, r3.id)
        self.assertEqual(len(r3.id), 36)

        self.assertLess(r1.created_at, r3.created_at)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'Only run this test when the storage is a file')
    def test_save_with_file(self):
        """Tests (save) function"""
        a1 = Review()
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
            a1.save(Review())

        if os.path.exists("file.json"):
            os.remove("file.json")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db'
                     or not storage._DBStorage__engine.table_names(),
                     'Only run this test when the storage is a database')
    def test_save_with_db(self):
        # Test save method updates updated_at attribute
        user = User(email="user@gmail.com", password="132",
                    first_name="user", last_name="user")
        user.save()
        state = State(name="state")
        state.save()
        city = City(name="city", state_id=state.id)
        city.save()
        place = Place(city_id=city.id, user_id=user.id, name="Sauna",
                      number_rooms=3, number_bathrooms=1, max_guest=4,
                      price_by_night=100)
        place.save()

        review = Review(text="Review", place_id=place.id, user_id=user.id)
        original_updated_at = review.updated_at

        review.save()

        self.assertNotEqual(original_updated_at, place.updated_at)
        self.assertIn(f"Review.{review.id}", storage.all())

    def test_str(self):
        """Tests __str__ function"""

        r1 = Review()
        r1_str = f"[{r1.__class__.__name__}] ({r1.id}) {r1.__dict__}"
        self.assertEqual(r1.__str__(), r1_str)

        self.assertEqual(type(r1.__str__()), str)

        # Adding new attribute to change r1.__dict__
        r1.name = "Review class"
        self.assertNotEqual(r1.__str__(), r1_str)

        with self.assertRaises(TypeError):
            r1.__str__(None)
        with self.assertRaises(TypeError):
            r1.__str__("None")

    def test_to_dict(self):
        """Tests to_dict function"""

        r1 = Review()
        review_attributes = ["place_id", "user_id", "text"]

        for attr in review_attributes:
            self.assertIn(attr, Review.__dict__.keys())

        for attr in review_attributes:
            self.assertNotIn(attr, r1.to_dict())

        temp_dict1 = {'id': r1.id,
                      'created_at': r1.created_at.isoformat(),
                      'updated_at': r1.updated_at.isoformat(),
                      '__class__': r1.__class__.__name__
                      }

        self.assertEqual(r1.to_dict(), temp_dict1)
        self.assertNotEqual(r1.to_dict(), r1.__dict__)

        r1.name = "BaseModel class"
        self.assertNotEqual(r1.to_dict(), temp_dict1)

        temp_dict2 = {'id': r1.id,
                      'created_at': r1.created_at.isoformat(),
                      'updated_at': r1.updated_at.isoformat(),
                      '__class__': r1.__class__.__name__,
                      "name": "BaseModel class"}

        self.assertEqual(r1.to_dict(), temp_dict2)

        r1.name = "Test Man"
        self.assertIn("name", r1.to_dict())

        # Tests that created_at and updated_at from to_dict() function
        # Matching iso format
        self.assertEqual(r1.created_at,
                         datetime.fromisoformat(temp_dict1["created_at"]))

        self.assertEqual(r1.created_at,
                         datetime.strptime(temp_dict1["created_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))

        self.assertEqual(r1.updated_at,
                         datetime.fromisoformat(temp_dict1["updated_at"]))

        self.assertEqual(r1.updated_at,
                         datetime.strptime(temp_dict1["updated_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        with self.assertRaises(TypeError):
            r1.to_dict(None)
        with self.assertRaises(TypeError):
            r1.to_dict("None")

    def test_delete_method(self):
        """Test delete method removes instance from storage"""
        user = User(email="user@gmail.com", password="132",
                    first_name="user", last_name="user")
        user.save()
        state = State(name="state")
        state.save()
        city = City(name="city", state_id=state.id)
        city.save()
        place = Place(city_id=city.id, user_id=user.id, name="Sauna",
                      number_rooms=3, number_bathrooms=1, max_guest=4,
                      price_by_night=100)
        place.save()

        review = Review(text="Review", place_id=place.id, user_id=user.id)

        review.save()
        review.delete()
        self.assertNotIn(f"Review.{review.id}", storage.all())

        if os.path.exists("file.json"):
            os.remove("file.json")
