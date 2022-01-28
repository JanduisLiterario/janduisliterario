import sqlite3
from app import app
from flask import g

DATABASE = './app/database/database.db'

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  
  return d

def get_db():
  db = sqlite3.connect(DATABASE)
  db.row_factory = dict_factory
  
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  
  if db is not None:
    db.close()