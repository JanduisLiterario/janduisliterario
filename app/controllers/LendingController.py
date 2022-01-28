from sqlite3.dbapi2 import Connection, Error
from app.models.lending import Lending

class LendingController():

  def __init__(self, db: Connection) -> None:
    self.db = db
    self.cursor = db.cursor()
  
  def get_one(self, lending_id: int) -> dict or None:
    sql = """
    select 
    lending.id, lending.created_at, lending.valid_at, lending.user_id, lending.book_id,
    users.nome, users.email,
    books.titulo
    from lending
    join users
    on lending.user_id = users.id
    join books
    on lending.book_id = books.id
    where lending.id = ?
    and lending.id not in (
      select lending_id from devolution
    );
    """

    self.cursor.execute(sql, (lending_id,))

    return self.cursor.fetchone()

  def get_abuses(self):
    sql = """
    select count(*) as 'amount', lending.user_id, lending.book_id,
    users.nome, books.titulo
    from lending
    join users
    on lending.user_id = users.id
    join books
    on lending.book_id = books.id
    group by lending.book_id, lending.user_id
    having amount >= 5;
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()

  def get_my_lendings(self, user_id: int) -> list:
    sql = """
    select
    books.*,
    lending.id as 'lending_id', lending.created_at 'data_do_emprestimo', lending.valid_at as 'data_validade_emprestimo',
    case
    	when lending.id not in (select lending_id from devolution) and lending.valid_at < (datetime('now', 'localtime')) then 'atrasado'
    	when lending.id not in (select lending_id from devolution) then false
      else true
    end as 'devolvido'
    from lending
    join users
    on lending.user_id = users.id
    join books
    on lending.book_id = books.id
    where lending.user_id = ?
    order by lending.created_at desc;
    """

    self.cursor.execute(sql, (user_id,))

    return self.cursor.fetchall()

  def get_all_per_book(self, book_id: int) -> list:
    sql = """
    select 
    lending.id, lending.created_at, lending.valid_at,
    users.nome, books.titulo, 
    CASE 
    	when lending.id in (select devolution.lending_id from devolution) then true
      else false
    end as 'devolvido'
    from lending
    join users
    on lending.user_id = users.id
    join books
    on lending.book_id = books.id
    where books.id = ?
    order by devolvido asc;
    """

    self.cursor.execute(sql, (book_id,))

    return self.cursor.fetchall()

  def create_lending(self, lending: Lending) -> int:
    sql = """
    insert into lending
    (user_id, book_id)
    values
    (?, ?);
    """

    try:
      self.cursor.execute(sql, (
        lending.user_id,
        lending.book_id
      ))

      self.db.commit()

      return self.cursor.lastrowid
    except Error as err:
      print(err)
      return None


    
  def verify_lending_book(self, book_id: int) -> dict or None:
    """ Esta funcao verifica se um determinado livro que foi emprestado ja foi devolvido

    Args:
      book_id (int): ID do livro

    Returns:
      dict or None: 
        - Caso o livro ainda nao tenha sido devolvido, os dados do emprestimo serao retornados
        - Caso a devoluçao tenha acontecido, retornara None
    """

    sql = """
    select *
    from lending
    where lending.book_id = ?
    and lending.id not in (select devolution.lending_id from devolution);
    """

    self.cursor.execute(sql, (book_id,))

    return self.cursor.fetchone()

  def get_all_late_lendings(self):
    sql = """
    select 
    lending.*, 
    books.titulo, 
    users.nome, users.email
    from lending
    join users
    on lending.user_id = users.id
    join books
    on lending.book_id = books.id
    where DATE(valid_at) <= DATE((datetime('now', 'localtime')));
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()

  def get_count_all(self) -> list:
    sql = """
    select count(*) as total
    from lending
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()

  def get_lendings_per_month(self) -> list:

    lendingspermonth = []

    sql = """
    SELECT count(*) as janeiro
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-01-01' AND '2022-02-01'
    """

    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as fevereiro
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-02-01' AND '2022-03-01'
    """

    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as marco
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-03-01' AND '2022-04-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as abril
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-04-01' AND '2022-05-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as maio
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-05-01' AND '2022-06-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as junho
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-06-01' AND '2022-07-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as julho
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-05-01' AND '2022-06-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as agosto
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-08-01' AND '2022-09-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as setembro
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-09-01' AND '2022-10-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as outubro
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-10-01' AND '2022-11-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as novembro
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-11-01' AND '2022-12-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as dezembro
    FROM lending 
    WHERE created_at 
    BETWEEN '2022-12-01' AND '2023-01-01'
    """
    self.cursor.execute(sql)

    lendingspermonth.append(self.cursor.fetchall())

    return lendingspermonth
  
  def people_served(self):

    peoples_served_list = []

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as janeiro
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '01' AND '02';
    """

    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as fevereiro
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '02' AND '03';
    """

    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as marco
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at)) 
    BETWEEN '03' AND '04';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as abril
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '04' AND '05';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as maio
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '05' AND '06';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as junho
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '06' AND '07';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as julho
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '07' AND '08';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as agosto
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '08' AND '09';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as setembro
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '09' AND '10';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as outubro
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))
    BETWEEN '10' AND '11';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as novembro
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at)) 
    BETWEEN '11' AND '12'
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())

    sql = """
    SELECT COUNT( DISTINCT(lending.user_id) ) as dezembro
    FROM lending 
    WHERE strftime('%m', DATETIME(created_at))  
    BETWEEN '12' AND '01';
    """
    self.cursor.execute(sql)

    peoples_served_list.append(self.cursor.fetchone())
  
    return peoples_served_list