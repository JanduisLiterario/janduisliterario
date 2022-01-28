from sqlite3.dbapi2 import Connection
from app.models.book import Book

class BookController():

  def __init__(self, db_connection: Connection) -> None:
    self.db = db_connection
    self.cursor = self.db.cursor()

  def create_book(self, book: Book) -> int:
    sql = """
    insert into books
    (titulo, descricao, autor, ano_lancamento, caminho_imagem, user_id)
    values
    (?, ?, ?, ?, ?, ?);
    """

    self.cursor.execute(sql, (
      book.titulo,
      book.descricao,
      book.autor,
      book.ano_lancamento,
      book.caminho_imagem,
      book.user_id
    ))

    self.db.commit()

    return self.cursor.lastrowid
  
  def get_all(self) -> list:
    sql = """
    select *,
    case
	    when id in (
    	  select book_id
		    from lending
		    where lending.id not in (select devolution.lending_id from devolution)
      ) then false
      else true
    end as 'disponivel'
    from books;
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()

  def get_count_all(self) -> list:
    sql = """
    select count(*) as total
    from books
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()
  
  def get_one(self, book_id: int) -> dict:
    # salvando busca anterior:
    #"""
    #select *
    #from books
    #where id = ?;
    #"""
    sql = """
    select *,
    case
	    when id in (
    	  select book_id
		    from lending
		    where lending.id not in (select devolution.lending_id from devolution)
      ) then false
      else true
    end as 'disponivel'
    from books 
    where id = ?;
    """

    self.cursor.execute(sql, (book_id,))

    return self.cursor.fetchone()

  def update_book(self, book: Book) -> int or None:
    sql = """
    update books
    set titulo = ?,
    descricao = ?,
    autor = ?,
    ano_lancamento = ?
    where id = ?;
    """

    self.cursor.execute(sql, (
      book.titulo,
      book.descricao,
      book.autor,
      book.ano_lancamento,
      book.id
    ))

    self.db.commit()

    return self.cursor.rowcount

  def delete_book(self, book_id: int) -> int or None:
    sql = """
    delete from books
    where id = ?;
    """

    self.cursor.execute(sql, (book_id,))

    self.db.commit()

    return self.cursor.rowcount

  def search_book(self, title: str) -> list:
    sql = """
    select *
    from books
    where books.titulo like ?;
    """

    self.cursor.execute(sql, (f"%{title}%",))

    return self.cursor.fetchall()

  def get_books_per_lending_date(self) -> list:
    sql = """
          select books.id, titulo, autor, ano_lancamento, descricao, caminho_imagem, count(*) as qtd,
          case
	          when books.id in (
    	        select book_id
		          from lending
		          where lending.id not in (select devolution.lending_id from devolution)
            ) then false
            else true
          end as 'disponivel'
          from lending 
          join books 
          where books.id = lending.book_id 
          group by titulo 
          order by qtd desc;
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()

  def get_books_per_date_created(self) -> list:
    sql = """
    select *,
    case
	    when books.id in (
        select book_id
		    from lending
		    where lending.id not in (select devolution.lending_id from devolution)
      ) then false
      else true
    end as 'disponivel'
    from books 
    order by created_at desc;

    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()

  def get_books_per_devolution_date(self) -> list:
    sql = """
      select DISTINCT books.*, devolution.data,
      case
	      when books.id in (
    	    select book_id
		      from lending
		      where lending.id not in (select devolution.lending_id from devolution)
        ) then false
        else true
      end as 'disponivel'
      from devolution
      join lending
      on lending.id = devolution.lending_id
      join books
      on lending.book_id = books.id
      order by devolution.data desc;
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()
  
  def get_books_awaiting(self) -> list:
    sql = """
    select DISTINCT book_id, max(devolution.data) as 'data'
    from lending
    join devolution
    on lending.id = devolution.lending_id
    where lending.id in (
    	select devolution.lending_id
      from devolution
    ) and lending.book_id not in (
    	select lending.book_id
      from lending
      where lending.id not in (
        select devolution.lending_id
      	from devolution
    	)
    )
    group by lending.book_id;
    """

    self.cursor.execute(sql)

    return self.cursor.fetchall()

  def get_books_per_month(self) -> list:

    bookspermonth = []

    sql = """
    SELECT count(*) as janeiro
    FROM books
    WHERE created_at 
    BETWEEN '2022-01-01' AND '2022-02-01'
    """

    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as fevereiro
    FROM books 
    WHERE created_at 
    BETWEEN '2022-02-01' AND '2022-03-01'
    """

    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as marco
    FROM books 
    WHERE created_at 
    BETWEEN '2022-03-01' AND '2022-04-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as abril
    FROM books
    WHERE created_at 
    BETWEEN '2022-04-01' AND '2022-05-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as maio
    FROM books 
    WHERE created_at 
    BETWEEN '2022-05-01' AND '2022-06-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as junho
    FROM books 
    WHERE created_at 
    BETWEEN '2022-06-01' AND '2022-07-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as julho
    FROM books 
    WHERE created_at 
    BETWEEN '2022-05-01' AND '2022-06-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as agosto
    FROM books
    WHERE created_at 
    BETWEEN '2022-08-01' AND '2022-09-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as setembro
    FROM books 
    WHERE created_at 
    BETWEEN '2022-09-01' AND '2022-10-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as outubro
    FROM books 
    WHERE created_at 
    BETWEEN '2022-10-01' AND '2022-11-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    sql = """
    SELECT count(*) as novembro
    FROM books
    WHERE created_at 
    BETWEEN '2022-11-01' AND '2022-12-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())
    sql = """
    SELECT count(*) as dezembro
    FROM books
    WHERE created_at 
    BETWEEN '2022-12-01' AND '2023-01-01'
    """
    self.cursor.execute(sql)

    bookspermonth.append(self.cursor.fetchall())

    return bookspermonth