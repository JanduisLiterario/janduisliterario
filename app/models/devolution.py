class Devolution():

  def __init__(self, lending_id: int, renew: bool = False) -> None:
    self.__id = 0
    self.__lending_id = lending_id
    self.__renew = renew
  
  def get_id(self) -> int:
    return self.__id
  
  def set_id(self, id: int) -> None:
    self.__id = id
  
  def get_lending_id(self) -> int:
    return self.__lending_id
  
  def set_lending_id(self, lending_id: int) -> None:
    self.__lending_id = lending_id

  def get_renew(self) -> bool:
    return self.__renew
  
  def set_renew(self, renew: bool) -> None:
    self.__renew = renew
  
  def __repr__(self) -> str:
    return f"<Lending(ID={self.__id}, Lending_ID={self.__lending_id}), Renew={self.__renew}>"

  id = property(fget=get_id, fset=set_id)
  lending_id = property(fget=get_lending_id, fset=set_lending_id)
  renew = property(fget=get_renew, fset=set_renew)