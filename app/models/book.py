import marshmallow as ma

class Book():

  def __init__(self, titulo: str, descricao: str, autor: str, ano_lancamento, caminho_imagem: str, user_id: int) -> None:
    self.__id = 0
    self.__titulo = titulo
    self.__descricao = descricao
    self.__autor = autor
    self.__ano_lancamento = ano_lancamento
    self.__caminho_imagem = caminho_imagem
    self.__user_id = user_id

  def get_id(self) -> int:
    return self.__id
  
  def set_id(self, id: int) -> None:
    self.__id = id
  
  def get_titulo(self) -> str:
    return self.__titulo
  
  def set_titulo(self, titulo: str) -> None:
    self.__titulo = titulo

  def get_descricao(self) -> str:
    return self.__descricao
  
  def set_descricao(self, descricao: str) -> None:
    self.__descricao = descricao
  
  def get_autor(self) -> str:
    return self.__autor

  def set_autor(self, autor: str) -> None:
    self.__autor = autor
  
  def get_ano_lancamento(self) -> str:
    return self.__ano_lancamento
  
  def set_ano_lancamento(self, ano_lancamento: str) -> None:
    self.__ano_lancamento = ano_lancamento

  def get_caminho_imagem(self) -> str:
    return self.__caminho_imagem
  
  def set_caminho_imagem(self, caminho_imagem: str) -> None:
    self.__caminho_imagem = caminho_imagem

  def get_user_id(self) -> str:
    return self.__user_id
  
  def set_user_id(self, user_id: str):
    self.__user_id = user_id

  def __repr__(self) -> str:
    return f"<Book(ID={self.__id}, Titulo={self.__titulo}, Descricao={self.__descricao}, Autor={self.__autor}, Ano_lancamento={self.__ano_lancamento}, Caminho_imagem={self.__caminho_imagem} User_ID={self.__user_id})>"
  
  id = property(fget=get_id, fset=set_id)
  titulo = property(fget=get_titulo, fset=set_titulo)
  descricao = property(fget=get_descricao, fset=set_descricao)
  autor = property(fget=get_autor, fset=set_autor)
  ano_lancamento = property(fget=get_ano_lancamento, fset=set_ano_lancamento)
  caminho_imagem = property(fget=get_caminho_imagem, fset=set_caminho_imagem)
  user_id = property(fget=get_user_id, fset=set_user_id)

class BookSchema(ma.Schema):
  class Meta:
    fields = ('id', 'titulo', 'descricao', 'autor', 'ano_lancamento', 'caminho_imagem', 'user_id')
  
book_schema = BookSchema()
books_schema = BookSchema(many=True)
