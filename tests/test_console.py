#!/usr/bin/python3
"""
A unit test module for the console (command interpreter).
"""

import os
import unittest
from io import StringIO
from unittest.mock import patch

import MySQLdb
import sqlalchemy
from console import HBNBCommand
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """
    Represents the test class for the HBNBCommand class.
    """

    @unittest.skipIf(
        os.getenv('MY_STORAGE_TYPE') == 'db', 'FileStorage test')
    def test_my_fs_create(self):
        """
        Tests the create command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            my_console = HBNBCommand()
            my_console.onecmd('create City name="MyCity"')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            my_console.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'MyCity'", cout.getvalue().strip())
            clear_stream(cout)
            my_console.onecmd('create User name="John" age=25 height=5.10')
            mdl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(cout)
            my_console.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'John'", cout.getvalue().strip())
            self.assertIn("'age': 25", cout.getvalue().strip())
            self.assertIn("'height': 5.10", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('MY_STORAGE_TYPE') != 'db', 'DBStorage test')
    def test_my_db_create(self):
        """
        Tests the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            my_console = HBNBCommand()
            # creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                my_console.onecmd('create User')
            # creating a User instance
            clear_stream(cout)
            my_console.onecmd(
                    'create User email="jane@gmail.com" password="789"')
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('MY_MYSQL_HOST'),
                port=3306,
                user=os.getenv('MY_MYSQL_USER'),
                passwd=os.getenv('MY_MYSQL_PWD'),
                db=os.getenv('MY_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('jane@gmail.com', result)
            self.assertIn('789', result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('MY_STORAGE_TYPE') != 'db', 'DBStorage test')
    def test_my_db_show(self):
        """
        Tests the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            my_console = HBNBCommand()
            # showing a User instance
            obj = User(email="jane@gmail.com", password="789")
            dbc = MySQLdb.connect(
                host=os.getenv('MY_MYSQL_HOST'),
                port=3306,
                user=os.getenv('MY_MYSQL_USER'),
                passwd=os.getenv('MY_MYSQL_PWD'),
                db=os.getenv('MY_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            my_console.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv('MY_MYSQL_HOST'),
                port=3306,
                user=os.getenv('MY_MYSQL_USER'),
                passwd=os.getenv('MY_MYSQL_PWD'),
                db=os.getenv('MY_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            my_console.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('jane@gmail.com', result)
            self.assertIn('789', result)
            self.assertIn('jane@gmail.com', cout.getvalue())
            self.assertIn('789', cout.getvalue())
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('MY_STORAGE_TYPE') != 'db', 'DBStorage test')
    def test_my_db_count(self):
        """
        Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            my_console = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv('MY_MYSQL_HOST'),
                port=3306,
                user=os.getenv('MY_MYSQL_USER'),
                passwd=os.getenv('MY_MYSQL_PWD'),
                db=os.getenv('MY_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            my_console.onecmd('create State name="MyState"')
            clear_stream(cout)
            my_console.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            my_console.onecmd('count State')
            cursor.close()
            dbc.close()
