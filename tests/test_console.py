#!/usr/bin/python3
"""A unit test module for the console (command interpreter).
"""
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Represents the test class for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_create_with_file(self):
        """Tests (create) function"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("creat")
            self.assertEqual(f.getvalue().strip(), "*** Unknown syntax: creat")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Base")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

        self.assertEqual(storage.all(), {})

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")

        self.assertEqual(len(storage.all()), 1)
        self.assertIn(f"BaseModel.{f.getvalue().strip()}", storage.all())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity name="wifi"')

        self.assertEqual(len(storage.all()), 2)
        self.assertIn(f"Amenity.{f.getvalue().strip()}", storage.all())
        key = f"Amenity.{f.getvalue().strip()}"

        self.assertEqual("wifi", storage.all()[key].name)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")

        self.assertEqual(len(storage.all()), 3)
        self.assertIn(f"State.{f.getvalue().strip()}", storage.all())

        with open("file.json", "r") as file:
            self.assertIn(f"State.{f.getvalue().strip()}", file.read())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Database test')
    def test_create_with_db(self):
        """Tests (create) function with database engine"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("creat")
            self.assertEqual(f.getvalue().strip(), "*** Unknown syntax: creat")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Base")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

        self.assertEqual(storage.all(), {})

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User email="user@email.com" password="123"')

        key = f"User.{f.getvalue().strip()}"
        print(key)
        self.assertEqual(len(storage.all()), 1)
        self.assertIn(key, storage.all())

        db = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id=%s', (f.getvalue().strip(),))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('user@email.com', result)
        self.assertIn('123', result)
        cursor.close()
        db.close()

    
