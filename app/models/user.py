import marshmallow as ma

class User():

  def __init__(self, nome: str, email: str, phone: str, password:str, nv_acess:int ) -> None:
    self.__id = 0
    self.__nome = nome
    self.__email = email
    self.__phone = phone
    self.__password = password
    self.nv_acess = nv_acess



  def get_id(self) -> int:
    return self.__id

  def set_id(self, id: int) -> None:
    self.__id = id

  def get_nome(self) -> str:
    return self.__nome
  
  def set_nome(self, nome: str) -> None:
    self.__nome = nome
  
  def get_email(self) -> str:
    return self.__email
  
  def set_email(self, email: str) -> None:
    self.__email = email

  def get_phone(self) -> str:
    return self.__phone
  
  def set_phone(self, phone: str) -> None:
    self.__phone = phone
  
  def get_password(self) -> str:
    return self.__password
  
  def set_password(self, password: str) -> None:
    self.__password = password
  
  id = property(fget=get_id, fset=set_id)
  nome = property(fget=get_nome, fset=set_nome)
  email = property(fget=get_email, fset=set_email)
  phone = property(fget=get_phone, fset=set_phone)
  password = property(fget=get_password, fset=set_password)
  

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'nome', 'email', 'phone', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)