#!/usr/bin/python3
"""This module contains TestDBStorage class"""
from models.engine.db_storage import DBStorage
from models import storage
import MySQLdb
from models.base_model import BaseModel, Base
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.state import State
import unittest
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db'
                 or not storage._DBStorage__engine.table_names(),
                 'Only run this test when the storage is a database')
class TestDBStorage(unittest.TestCase):
    """This class is for testing DBStorage class attributes and functions"""

    def setUp(self):
        """Setup data before each test method"""

        self.db_connection = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )

        self.cursor = self.db_connection.cursor()

    def tearDown(self):
        """Excutes data after each test method"""

        self.cursor.close()
        self.db_connection.close()

    def test_new(self):
        """Tests new() function"""

        my_cursor = self.cursor

        user = User(
            email="mohamed@gmail.com",
            password="123456",
            first_name="Mohamed",
            last_name="Ali"
        )

        self.assertFalse(user in storage.all().values())
        storage.new(user)
        self.assertTrue(user in storage.all().values())

        my_cursor.execute(
            "SELECT * FROM users WHERE id=%s", (user.id,))

        self.assertEqual(my_cursor.rowcount, 0)
        storage.save()
        self.db_connection.commit()

        my_cursor.execute(
            "SELECT * FROM users WHERE id=%s", (user.id,))

        self.assertEqual(my_cursor.rowcount, 1)

    def test_delete(self):
        """Tests delete method"""

        amenity = Amenity(name="Wifi")

        storage.new(amenity)
        storage.save()

        self.assertIn(amenity, storage.all().values())

        amenity.delete()

        self.assertNotIn(amenity, storage.all().values())

    def test_reload(self):
        """Tests reload method"""

        my_cursor = self.cursor

        Base.metadata.drop_all(storage._DBStorage__engine)

        my_cursor.execute("SHOW TABLES")
        self.assertEqual(my_cursor.rowcount, 0)

        storage.reload()
        self.db_connection.commit()
        my_cursor.execute("SHOW TABLES")
        self.assertEqual(my_cursor.rowcount, 7)
        self.assertIn(("users",), my_cursor.fetchall())

        amenity = Amenity(name="Pets")

        my_cursor.execute("INSERT INTO amenities VALUES(%s, %s, %s, %s)",
                          (amenity.id, amenity.created_at,
                           amenity.updated_at, amenity.name))

        self.assertNotIn(f"Amenity.{amenity.id}", storage.all())

        self.db_connection.commit()

        storage.reload()
        self.assertIn(f"Amenity.{amenity.id}", storage.all())
