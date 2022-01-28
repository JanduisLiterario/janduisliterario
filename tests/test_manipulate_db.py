import unittest

from app.database.connection import get_db
from app.database.createdb import create_tables, drop_tables

class TestManipulateDBMethods(unittest.TestCase):

  def test_create_tables(self):
    create_tables(get_db())

    self.assertEqual(0, 0)
  
  def test_drop_tables(self):
    drop_tables(get_db())
    
    self.assertEqual(0, 0)