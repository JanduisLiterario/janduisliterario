import unittest

from app.database.connection import get_db
from app.controllers.AccessController import AccessController

class TestAccessMethods(unittest.TestCase):

  def test_create_access(self):
    controller = AccessController(get_db())
    access_id = controller.create_access( 1 )

    self.assertIsNotNone(access_id)