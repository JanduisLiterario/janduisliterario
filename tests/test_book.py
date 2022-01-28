import unittest
from app.database.connection import get_db
from app.database.createdb import create_tables, drop_tables

from app.models.book import Book
from app.controllers.BookController import BookController


class TestBookMethods(unittest.TestCase):
  controller = BookController(get_db())
  
  def test_create_book(self):
    book = Book("Harry", "", "", 2000, 1)

    result = self.controller.create_book( book )

    self.assertIsNotNone( result )
  
  def test_get_all_books(self):
    result = self.controller.get_all()

    self.assertGreater(len(result), 0)

  def test_get_one_book(self):
    result = self.controller.get_one(1)

    self.assertIsNotNone(result)

  def test_update_book(self):
    book = Book("Harry", "NICE", "PERFECT", 2000, 1)
    book.id = 1

    result = self.controller.update_book(book)

    self.assertGreater(result, 0)
  
  def test_delete_book(self):
    result = self.controller.delete_book(1)

    self.assertGreater(result, 0)