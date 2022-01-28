import unittest
from app.database.connection import get_db
from app.database.createdb import create_tables, drop_tables

from app.models.user import User
from app.controllers.UserController import UserController

class TestUserMethods(unittest.TestCase):

  def test_create_user(self):
    controller = UserController(get_db())
    user = User("Jerbeson", "j333", "3333", "aa", "aa", "aa", True)

    result = controller.create_user(user)

    self.assertIsNotNone(result)

  def test_user_exists(self):
    controller = UserController(get_db())
    user = User("Jerbeson", "j333", "3333", "aa", "aa", "aa", True)

    result = controller.user_exists(user)

    self.assertIsNotNone(result)
