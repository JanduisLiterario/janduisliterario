from sqlite3.dbapi2 import Connection, Error
from app.models.lending import Lending

class AwaitingController():

  def __init__(self, db: Connection) -> None:
    self.db = db
    self.cursor = db.cursor()
  
  def obter(self, awaiting_id: int) -> dict:
    sql = """
    select *
    from awaiting
    where id = ?;
    """

    self.cursor.execute(sql, (awaiting_id,))

    return self.cursor.fetchone()

  def create_awaiting_list(self, awaiting: Lending) -> int or None:
    sql = """
    insert into awaiting
    (user_id, book_id)
    values
    (?, ?);
    """

    try:
      self.cursor.execute(sql, (
        awaiting.user_id,
        awaiting.book_id
      ))

      self.db.commit()

      return self.cursor.lastrowid
    except Error as err:
      print(err)
      return None
  
  def delete(self, awaiting_id: int) -> int:
    sql = """
    delete from awaiting
    where id = ?;
    """

    self.cursor.execute(sql, (awaiting_id,))

    self.db.commit()
    
    return self.cursor.rowcount

  def verify_awaiting_list_per_book(self, book_id: int) -> list or None:
    """ Esta funcao permite verificar se existe alguem na fila de espera por um determinado livro

    Args:
      book_id (int): ID do livro

    Returns:
      list or None: 
        - Se tiver uma ou mais pessoas na fila de espera, retornara uma lista com algumas informacoes
        - Caso contrario, retorna None
    """

    sql = """
    select awaiting.id, awaiting.created_at, awaiting.user_id, awaiting.book_id, books.titulo,
    users.nome, users.email
    from awaiting
    join users
    on awaiting.user_id = users.id
    join books
    on awaiting.book_id = books.id
    where awaiting.book_id = ?
    order by awaiting.created_at asc;
    """

    self.cursor.execute(sql, (book_id,))

    return self.cursor.fetchall()