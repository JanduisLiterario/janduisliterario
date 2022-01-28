from sqlite3.dbapi2 import Connection, Error
from app.database.connection import get_db, close_connection

class AccessController():

  def __init__(self, db: Connection) -> None:
    self.db = db
    self.cursor = db.cursor()

  def create_access(self, user_id: int) -> int:
    sql = """
    INSERT INTO access
    (user_id)
    VALUES
    (?);
    """

    try:
      self.cursor.execute(sql, (user_id,))

      self.db.commit()

      return self.cursor.lastrowid    
    except Error as err:
      print(err)
      return None
