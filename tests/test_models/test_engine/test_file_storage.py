#!/usr/bin/python3
"""This module contains TestFileStorage class"""
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.state import State
import unittest
import os


class TestFileStorage(unittest.TestCase):
    """This class is for testing FileStorage class attributes and functions"""

    def setUp(self):
        """Setup data before each test method"""

        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Excutes data after each test method"""

        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_new(self):
        """Tests new() function"""

        storage = FileStorage()
        self.assertEqual(storage.all(), {})

        b = BaseModel()
        storage.new(b)
        self.assertEqual(len(storage.all()), 1)
        self.assertIn(f"BaseModel.{b.id}", storage.all().keys())
        self.assertIn(b, storage.all().values())

        u = User()
        storage.new(u)
        self.assertEqual(len(storage.all()), 2)
        self.assertIn(f"User.{u.id}", storage.all().keys())
        self.assertIn(u, storage.all().values())

        storage.new(BaseModel())
        self.assertEqual(len(storage.all()), 3)
        storage.new(User())
        self.assertEqual(len(storage.all()), 4)
        storage.new(City())
        self.assertEqual(len(storage.all()), 5)
        storage.new(Place())
        self.assertEqual(len(storage.all()), 6)
        storage.new(Review())
        self.assertEqual(len(storage.all()), 7)
        storage.new(Amenity())
        self.assertEqual(len(storage.all()), 8)

        c = City()
        storage.new(c)
        self.assertIn(f"City.{c.id}", storage.all().keys())
        self.assertIn(c, storage.all().values())

        p = Place()
        storage.new(p)
        self.assertIn(f"Place.{p.id}", storage.all().keys())
        self.assertIn(p, storage.all().values())

        r = Review()
        storage.new(r)
        self.assertIn(f"Review.{r.id}", storage.all().keys())
        self.assertIn(r, storage.all().values())

        a = Amenity()
        storage.new(a)
        self.assertIn(f"Amenity.{a.id}", storage.all().keys())
        self.assertIn(a, storage.all().values())

        s = State()
        storage.new(s)
        self.assertIn(f"State.{s.id}", storage.all().keys())
        self.assertIn(s, storage.all().values())

        with self.assertRaises(TypeError):
            storage.new(BaseModel(), 4)

        with self.assertRaises(AttributeError):
            storage.new(None)

    def test_save(self):
        """Tests save() function"""

        storage = FileStorage()

        self.assertFalse(os.path.exists("file.json"))

        storage.save()

        self.assertTrue(os.path.exists("file.json"))

        with open("file.json", "r") as file1:
            file_content = file1.read()

        self.assertEqual(file_content, "{}")

        b = BaseModel()
        storage.new(b)
        self.assertEqual(len(storage.all()), 1)

        b.save()

        with open("file.json", "r") as file2:
            file_content = file2.read()

        self.assertIn(f"BaseModel.{b.id}", file_content)

        u = User()
        storage.new(u)
        storage.save()
        with open("file.json", "r") as file3:
            file_content = file3.read()
        self.assertIn(f"User.{u.id}", file_content)

        c = City()
        storage.new(c)
        storage.save()
        with open("file.json", "r") as file4:
            file_content = file4.read()
        self.assertIn(f"City.{c.id}", file_content)

        p = Place()
        storage.new(p)
        storage.save()
        with open("file.json", "r") as file5:
            file_content = file5.read()
        self.assertIn(f"Place.{p.id}", file_content)

        r = Review()
        storage.new(r)
        storage.save()
        with open("file.json", "r") as file6:
            file_content = file6.read()
        self.assertIn(f"Review.{r.id}", file_content)

        a = Amenity()
        storage.new(a)
        storage.save()
        with open("file.json", "r") as file7:
            file_content = file7.read()
        self.assertIn(f"Amenity.{a.id}", file_content)

        s = State()
        storage.new(s)
        storage.save()
        with open("file.json", "r") as file8:
            file_content = file8.read()
        self.assertIn(f"State.{s.id}", file_content)

        with self.assertRaises(TypeError):
            storage.save(None)

        with self.assertRaises(TypeError):
            storage.save(BaseModel(), 10)

    def test_reload(self):
        """Tests reload() function"""

        storage = FileStorage()

        self.assertEqual(storage.all(), {})

        b = BaseModel()
        storage.new(b)
        storage.save()
        storage.reload()

        deserialized_objects = storage.all()
        self.assertIn(f"BaseModel.{b.id}", deserialized_objects)
        self.assertEqual(len(deserialized_objects), 1)

        u = User()
        storage.new(u)
        storage.save()
        storage.reload()

        deserialized_objects = storage.all()
        self.assertIn(f"User.{u.id}", deserialized_objects)
        self.assertEqual(len(deserialized_objects), 2)

        c = City()
        storage.new(c)
        storage.save()
        storage.reload()

        deserialized_objects = storage.all()
        self.assertIn(f"City.{c.id}", deserialized_objects)
        self.assertEqual(len(deserialized_objects), 3)

        p = Place()
        storage.new(p)
        storage.save()
        storage.reload()

        deserialized_objects = storage.all()
        self.assertIn(f"Place.{p.id}", deserialized_objects)
        self.assertEqual(len(deserialized_objects), 4)

        r = Review()
        storage.new(r)
        storage.save()
        storage.reload()

        deserialized_objects = storage.all()
        self.assertIn(f"Review.{r.id}", deserialized_objects)
        self.assertEqual(len(deserialized_objects), 5)

        a = Amenity()
        storage.new(a)
        storage.save()
        storage.reload()

        deserialized_objects = storage.all()
        self.assertIn(f"Amenity.{a.id}", deserialized_objects)
        self.assertEqual(len(deserialized_objects), 6)

        s = State()
        storage.new(s)
        storage.save()
        storage.reload()

        deserialized_objects = storage.all()
        self.assertIn(f"State.{s.id}", deserialized_objects)
        self.assertEqual(len(deserialized_objects), 7)

        with self.assertRaises(TypeError):
            storage.reload(None)
        with self.assertRaises(TypeError):
            storage.reload(s)

        FileStorage._FileStorage__objects = {}
        os.remove("file.json")
        storage.reload()
        self.assertEqual(storage.all(), {})

    def test_all(self):
        """Tests all() function"""

        storage = FileStorage()

        self.assertEqual(storage.all(), {})
        self.assertEqual(type(storage.all()), dict)

        b = BaseModel()
        storage.new(b)
        self.assertEqual(len(storage.all()), 1)
        self.assertIn(f"BaseModel.{b.id}", storage.all().keys())
        self.assertIn(b, storage.all().values())

        u = User()
        storage.new(u)
        self.assertEqual(len(storage.all()), 2)
        self.assertIn(f"User.{u.id}", storage.all().keys())
        self.assertIn(u, storage.all().values())

        c = City()
        storage.new(c)
        self.assertEqual(len(storage.all()), 3)
        self.assertIn(f"City.{c.id}", storage.all().keys())
        self.assertIn(c, storage.all().values())

        p = Place()
        storage.new(p)
        self.assertEqual(len(storage.all()), 4)
        self.assertIn(f"Place.{p.id}", storage.all().keys())
        self.assertIn(p, storage.all().values())

        r = Review()
        storage.new(r)
        self.assertEqual(len(storage.all()), 5)
        self.assertIn(f"Review.{r.id}", storage.all().keys())
        self.assertIn(r, storage.all().values())

        a = Amenity()
        storage.new(a)
        self.assertEqual(len(storage.all()), 6)
        self.assertIn(f"Amenity.{a.id}", storage.all().keys())
        self.assertIn(a, storage.all().values())

        s = State()
        storage.new(s)
        self.assertEqual(len(storage.all()), 7)
        self.assertEqual(len(storage.all(State)), 1)
        self.assertIn(f"State.{s.id}", storage.all().keys())
        self.assertIn(s, storage.all().values())

        self.assertTrue(storage.all() is FileStorage._FileStorage__objects)
        self.assertTrue(storage.all() == FileStorage._FileStorage__objects)

    def test_delete(self):
        """Tests delete method"""

        storage = FileStorage()

        base = BaseModel()
        storage.new(base)

        self.assertIn(base, storage.all().values())

        storage.delete(base)

        self.assertNotIn(base, storage.all().values())
