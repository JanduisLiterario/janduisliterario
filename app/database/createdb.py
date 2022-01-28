from app.database.connection import get_db, close_connection
from sqlite3 import Connection

# Funcao que permite fazer a criacao de todas as tabelas no banco
def create_tables(db: Connection):
  sql = """
    CREATE TABLE users (
      id integer primary key autoincrement,
      nome varchar not null,
      email varchar not null unique,
      matricula varchar not null unique,
      curso varchar not null,
      nv_acess integer not null,
      campus varchar not null,
      matriculado bool not null
    );

    CREATE TABLE access (
      id integer primary key autoincrement,
      created_at datetime default (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
      user_id integer,

      foreign key (user_id) references users(id)
    );

    CREATE TABLE books (
      id integer primary key autoincrement,
      titulo varchar(30) not null,
      descricao text,
      autor varchar,
      ano_lancamento integer,
      caminho_imagem varchar not null,
      created_at datetime default (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
      user_id integer,

      foreign key (user_id) references users(id)
    );

    CREATE TABLE lending (
      id integer primary key autoincrement,
      created_at datetime default (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
      valid_at datetime default (
        datetime(
          'now',
          'localtime',
          'start of day',
          '+1 month',
          '+1 day',
          '-1 minute'
        )
      ),
      user_id integer,
      book_id integer,

      foreign key (user_id) references users (id),
      foreign key (book_id) references books (id)
    );

    CREATE TABLE awaiting (
      id integer primary key autoincrement,
      created_at datetime default (datetime('now', 'localtime')),
      user_id integer,
      book_id integer,

      foreign key (user_id) references users (id),
      foreign key (book_id) references books (id)
    );

    CREATE TABLE devolution (
      id integer primary key autoincrement,
      data datetime default (datetime('now', 'localtime')),
      lending_id integer,
      renew bool not null,

      foreign key (lending_id) references lending (id)
    );
  """

  cursor = db.cursor()
  cursor.executescript(sql)

  db.commit()

  return cursor.lastrowid

# Funcao que permite apagar todas as tabelas do banco
def drop_tables(db: Connection):
  sql = """
  drop table if exists users;
  drop table if exists access;
  drop table if exists books;
  drop table if exists lending;
  drop table if exists awaiting;
  drop table if exists devolution;
  """

  cursor = db.cursor()
  cursor.executescript(sql)

  db.commit()

  return True