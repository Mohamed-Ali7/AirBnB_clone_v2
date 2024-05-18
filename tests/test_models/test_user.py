#!/usr/bin/python3
"""This module contains TestUser class to test User class"""
import unittest
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.base_model import BaseModel
from datetime import datetime
import os
from models import storage


class TestUser(unittest.TestCase):
    """This class is for testing User class attributes and functions"""

    def test_instantiation(self):
        """Tests creating an instance of User class"""

        u1 = User()
        old_updated_at = u1.updated_at
        u1_dict = u1.to_dict()

        self.assertEqual(len(u1.id), 36)
        self.assertTrue(isinstance(u1, BaseModel))

        # Checking attributes types
        self.assertEqual(type(u1.id), str)
        self.assertEqual(type(u1.created_at), datetime)
        self.assertEqual(type(u1.updated_at), datetime)
        self.assertEqual(type(u1_dict["created_at"]), str)
        self.assertEqual(type(u1_dict["updated_at"]), str)

        self.assertLess(u1.created_at, u1.updated_at)

        # Checking __class__ attribute in __dict__ and to_dict()
        self.assertNotEqual(u1.created_at, old_updated_at)
        self.assertTrue("__class__" in u1_dict)
        self.assertTrue("__class__" not in u1.__dict__)

        # Creating a new instance using kwargs
        u2 = User(**u1_dict)

        self.assertTrue("__class__" in u2.to_dict())
        self.assertTrue("__class__" not in u2.__dict__)

        self.assertTrue(u2.to_dict()["__class__"], "BaseModel")

        # Checking datetime attributes types
        self.assertEqual(type(u2.created_at), datetime)
        self.assertEqual(type(u2.updated_at), datetime)

        # Checking if the two instances are the same object
        self.assertTrue(u1 is not u2)
        self.assertTrue(u1 != u2)

        # Checking if the two instance's attributes are equal
        self.assertEqual(u1.id, u2.id)
        self.assertEqual(u1.to_dict(), u2.to_dict())

        # Set new attribute to u2 instance
        u2.name = "User class"
        self.assertNotEqual(u1.to_dict(), u2.to_dict())
        self.assertTrue("name" in u2.to_dict())
        self.assertTrue("name" not in u1.to_dict())

        # Tests that the each new created instance has a unique id
        u3 = User()
        self.assertNotEqual(u2.id, u3.id)
        self.assertEqual(len(u3.id), 36)

        self.assertLess(u1.created_at, u3.created_at)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'Only run this test when the storage is a file')
    def test_save_with_file(self):
        """Tests (save) function"""
        user = User(email="user@gmail.com", password="132",
                    first_name="user", last_name="user")
        old_updated_at = user.updated_at

        self.assertTrue(not os.path.exists("file.json"))

        # Tests if updated_at attribute has changed after calling save() method
        user.save()
        self.assertNotEqual(old_updated_at, user.updated_at)
        self.assertIn(f"{user.__class__.__name__}.{user.id}", storage.all())

        self.assertTrue(os.path.exists("file.json"))

        with self.assertRaises(TypeError):
            user.save(None)
        with self.assertRaises(TypeError):
            user.save("None")

        if os.path.exists("file.json"):
            os.remove("file.json")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db'
                     or not storage._DBStorage__engine.table_names(),
                     'Only run this test when the storage is a database')
    def test_save_with_db(self):
        # Test save method updates updated_at attribute
        user = User(email="user@gmail.com", password="132",
                    first_name="user", last_name="user")
        original_updated_at = user.updated_at

        user.save()
        self.assertNotEqual(original_updated_at, user.updated_at)
        self.assertIn(f"User.{user.id}", storage.all())

    def test_str(self):
        """Tests __str__ function"""

        u1 = User()
        u1_str = f"[{u1.__class__.__name__}] ({u1.id}) {u1.__dict__}"
        self.assertEqual(u1.__str__(), u1_str)

        self.assertEqual(type(u1.__str__()), str)

        # Adding new attribute to change u1.__dict__
        u1.name = "User class"
        self.assertNotEqual(u1.__str__(), u1_str)

        with self.assertRaises(TypeError):
            u1.__str__(None)
        with self.assertRaises(TypeError):
            u1.__str__("None")

    def test_to_dict(self):
        """Tests to_dict function"""

        u1 = User()
        user_attributes = [
            "email",
            "password",
            "first_name",
            "last_name"
        ]

        for attr in user_attributes:
            self.assertIn(attr, User.__dict__.keys())

        for attr in user_attributes:
            self.assertNotIn(attr, u1.to_dict())

        temp_dict1 = {'id': u1.id,
                      'created_at': u1.created_at.isoformat(),
                      'updated_at': u1.updated_at.isoformat(),
                      '__class__': u1.__class__.__name__
                      }

        self.assertEqual(u1.to_dict(), temp_dict1)
        self.assertNotEqual(u1.to_dict(), u1.__dict__)

        u1.name = "BaseModel class"
        self.assertNotEqual(u1.to_dict(), temp_dict1)

        temp_dict2 = {'id': u1.id,
                      'created_at': u1.created_at.isoformat(),
                      'updated_at': u1.updated_at.isoformat(),
                      '__class__': u1.__class__.__name__,
                      "name": "BaseModel class"}

        self.assertEqual(u1.to_dict(), temp_dict2)

        u1.first_name = "test"
        self.assertIn("first_name", u1.to_dict())

        # Tests that created_at and updated_at from to_dict() function
        # Matching iso format
        self.assertEqual(u1.created_at,
                         datetime.fromisoformat(temp_dict1["created_at"]))

        self.assertEqual(u1.created_at,
                         datetime.strptime(temp_dict1["created_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))

        self.assertEqual(u1.updated_at,
                         datetime.fromisoformat(temp_dict1["updated_at"]))

        self.assertEqual(u1.updated_at,
                         datetime.strptime(temp_dict1["updated_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        with self.assertRaises(TypeError):
            u1.to_dict(None)
        with self.assertRaises(TypeError):
            u1.to_dict("None")

    def test_delete_method(self):
        """Test delete method removes instance from storage"""
        user = User(email="user@gmail.com", password="132",
                    first_name="user", last_name="user")
        user_id = user.id

        user.save()
        user.delete()
        self.assertNotIn(f"Amenity.{user_id}", storage.all())

        if os.path.exists("file.json"):
            os.remove("file.json")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     'Only run this test when the storage is a db')
    def test_reviews_places_relationship(self):
        # Test relationship between User and Review
        user = User(email="user@gmail.com", password="132",
                    first_name="user", last_name="user")
        state = State(name="state")
        city = City(name="city")

        state.cities.append(city)

        review = Review(text="Review")

        place = Place(name="Sauna",
                      number_rooms=3, number_bathrooms=1, max_guest=4,
                      price_by_night=100)

        place.reviews.append(review)
        city.places.append(place)
        user.reviews.append(review)
        user.places.append(place)
        user.save()

        self.assertIn(f"Review.{review.id}", storage.all())
        self.assertEqual(review.user_id, user.id)
        self.assertIn(review, user.reviews)

        self.assertIn(f"Place.{place.id}", storage.all())
        self.assertEqual(place.user_id, user.id)
        self.assertIn(place, user.places)
