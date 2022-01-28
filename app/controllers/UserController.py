from sqlite3 import Connection
from sqlite3.dbapi2 import Error
from app.models.user import User

class UserController():

  def __init__(self, db_connection: Connection) -> None:
    self.db = db_connection
    self.cursor = self.db.cursor()

  def get_all_emails(self):
    sql = """
    select email
    from users;
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()

  def get_one(self, user_id: int) -> dict:
    sql = """
    select * 
    from users
    where id = ?;
    """

    self.cursor.execute(sql, (user_id,))

    return self.cursor.fetchone()

  def create_user(self, user: User) -> int:
    sql = """
    insert into users
    (nome, email, phone, password, nv_acess)
    values
    (?, ?, ?, ?, ?);
    """

    try:
      self.cursor.execute(sql, (
        user.nome,
        user.email,
        user.phone,
        user.password,
        user.nv_acess,
      ))

      self.db.commit()
      
      return self.cursor.lastrowid
    except Error as err:
      print(err)
      return None
  
  def user_exists(self, user: User) -> dict:
    sql = """
    select id, email
    from users
    where matricula = ?;
    """

    self.cursor.execute(sql, (
      user.matricula,
    ))

    return self.cursor.fetchone()
  
  def set_new_adm(self, user_id: str) -> int:
    sql = """
    update users
    set nv_acess = 2
    where id = ? and nv_acess != 0;
    """

    self.cursor.execute(sql, (user_id,))

    self.db.commit()

    return self.cursor.rowcount

    
  def get_count_all(self) -> list:
    sql = """
    select count(*) as total
    from users
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()


  def autenticar(self, email, senha):
        sql = "SELECT * FROM users WHERE email=? AND password=?"

        cursor = self.db.cursor()
        cursor.execute(sql, (email,senha,))
        return cursor.fetchone()