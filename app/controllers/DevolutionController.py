from sqlite3.dbapi2 import Connection, Error
from app.models.devolution import Devolution

class DevolutionController():

  def __init__(self, db: Connection) -> None:
    self.db = db
    self.cursor = db.cursor()

  def register_devolution(self, devolution: Devolution) -> int or None:
    sql = """
    insert into devolution
    (lending_id, renew)
    values
    (?, ?);
    """

    try:
      self.cursor.execute(sql, (
        devolution.lending_id,
        devolution.renew
      ))

      self.db.commit()

      return self.cursor.lastrowid
    except Error as err:
      print(err)
      return None

  def get_my_devolutions(self, user_id: int) -> list:
    sql = """
    select 
    devolution.data as 'data_devolucao', devolution.renew as 'renovacao',
    lending.created_at 'data_do_emprestimo', lending.valid_at as 'data_validade_emprestimo',
    users.nome as 'nome_do_usuario',
    books.*
    from devolution
    join lending
    on devolution.lending_id = lending.id
    join users
    on lending.user_id = users.id
    join books
    on lending.book_id = books.id
    where lending.user_id = ?
    order by devolution.data desc;
    """

    self.cursor.execute(sql, (user_id,))

    return self.cursor.fetchall()