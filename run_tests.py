import unittest
from tests.test_lending import TestLendingMethods

from tests.test_user import TestUserMethods
from tests.test_book import TestBookMethods
from tests.test_access import TestAccessMethods
from tests.test_awaiting import TestAwaitingMethods
from tests.test_manipulate_db import TestManipulateDBMethods

def suite():
  suite = unittest.TestSuite()
  suite.addTest(TestManipulateDBMethods('test_drop_tables'))
  suite.addTest(TestManipulateDBMethods('test_create_tables'))
  suite.addTest(TestUserMethods('test_create_user'))
  suite.addTest(TestUserMethods('test_user_exists'))
  suite.addTest(TestAccessMethods('test_create_access'))
  suite.addTest(TestBookMethods('test_create_book'))
  suite.addTest(TestBookMethods('test_get_all_books'))
  suite.addTest(TestBookMethods('test_get_one_book'))
  suite.addTest(TestBookMethods('test_update_book'))
  suite.addTest(TestAwaitingMethods('test_add_user_in_awaiting_list'))
  suite.addTest(TestAwaitingMethods('test_verify_awaiting_list_per_book'))
  suite.addTest(TestLendingMethods('test_create_lending'))
  suite.addTest(TestLendingMethods('test_verify_lending_book'))
  suite.addTest(TestBookMethods('test_delete_book'))

  return suite

if( __name__ == '__main__'):
  runner = unittest.TextTestRunner(failfast=True, verbosity=2)
  runner.run(suite())