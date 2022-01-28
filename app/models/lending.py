class Lending():

  def __init__(self, user_id: int, book_id: int) -> None:
    self.__id = 0
    self.__user_id = user_id
    self.__book_id = book_id
  
  def get_id(self) -> int:
    return self.__id
  
  def set_id(self, id: int) -> None:
    self.__id = id
  
  def get_user_id(self) -> int:
    return self.__user_id
  
  def set_user_id(self, user_id: int) -> None:
    self.__user_id = user_id
  
  def get_book_id(self) -> int:
    return self.__book_id
  
  def set_book_id(self, book_id: int) -> None:
    self.__book_id = book_id
  
  def __repr__(self) -> str:
    return f"<Lending(ID={self.__id}, User_ID={self.__user_id}, Book_ID={self.__book_id})>"

  id = property(fget=get_id, fset=set_id)
  user_id = property(fget=get_user_id, fset=set_user_id)
  book_id = property(fget=get_book_id, fset=set_book_id)