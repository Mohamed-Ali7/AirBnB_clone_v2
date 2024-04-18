#!/usr/bin/python3
"""This module contains TestDBStorage class"""
from models import storage
import MySQLdb
from models.user import User
from models.amenity import Amenity
import unittest
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
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
            email="user@gmail.com",
            password="123456",
            first_name="user",
            last_name="user"
        )
        my_cursor.execute(
            "SELECT * FROM users WHERE id=%s", (user.id,))

        self.assertEqual(my_cursor.rowcount, 0)

        self.assertNotIn(user, storage.all().values())
        user.save()
        self.assertIn(user, storage.all().values())

        self.db_connection.commit()

        my_cursor.execute(
            "SELECT * FROM users WHERE id=%s", (user.id,))

        self.assertEqual(my_cursor.rowcount, 1)
        result = my_cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn(user.email, result)
        self.assertIn(user.password, result)

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

        amenity = Amenity(name="Pets")

        my_cursor.execute("INSERT INTO amenities VALUES(%s, %s, %s, %s)",
                          (amenity.id, amenity.created_at,
                           amenity.updated_at, amenity.name))

        self.assertNotIn(f"Amenity.{amenity.id}", storage.all())

        self.db_connection.commit()

        storage.reload()
        self.assertIn(f"Amenity.{amenity.id}", storage.all())

    def test_new_and_save(self):
        '''testing  the new and save methods'''
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'jack',
                           'last_name': 'bond',
                           'email': 'jack@bond.com',
                           'password': 12345})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        old_count = cur.fetchall()
        cur.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        new_count = cur.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)
        cur.close()
        db.close()
