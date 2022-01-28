import unittest

from app.database.connection import get_db
from app.models.lending import Lending
from app.controllers.AwaitingController import AwaitingController

class TestAwaitingMethods(unittest.TestCase):

  def test_add_user_in_awaiting_list(self):
    controller = AwaitingController(get_db())
    lending = Lending(1, 1)

    result = controller.create_awaiting_list(lending)

    self.assertIsNotNone(result)
  
  def test_verify_awaiting_list_per_book(self):
    controller = AwaitingController(get_db())

    result = controller.verify_awaiting_list_per_book(1)

    self.assertIsNotNone(result)