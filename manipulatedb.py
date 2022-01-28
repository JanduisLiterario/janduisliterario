from app.database.connection import get_db
from app.controllers.LendingController import LendingController

controller = LendingController(get_db())

data = controller.get_all_late_lendings()

emails = list(map( lambda x: x.get('email'), data ))
livros = list(map( lambda x: x.get('titulo'), data ))

for email, livros in zip(emails, livros):
  print( email, livros )
  