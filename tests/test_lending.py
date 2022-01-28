import unittest

from app.database.connection import get_db
from app.models.lending import Lending
from app.controllers.LendingController import LendingController

class TestLendingMethods(unittest.TestCase):

  def test_create_lending(self):
    controller = LendingController(get_db())
    lending = Lending(1, 1)

    result = controller.create_lending(lending)

    self.assertIsNotNone(result)

  def test_verify_lending_book(self):
    controller = LendingController(get_db())

    result = controller.verify_lending_book(1)

    self.assertIsNotNone(1)