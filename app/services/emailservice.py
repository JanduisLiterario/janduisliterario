import smtplib

from email.message import EmailMessage
from datetime import datetime

class EmailService():

  def __init__(self, username: str, password: str, list_to_addrs: list, book_name: str = "", server: str = "smtp.office365.com") -> None:
    self.__server = smtplib.SMTP(server, 587)
    self.__username = username
    self.__password = password
    self.__list_to_addrs = list_to_addrs
    self.__book_name = book_name

  def set_book_name(self, book_name: str) -> None:
    self.__book_name = book_name

  def send_message_new_book(self):
    try:
      self.__server.ehlo()
      self.__server.starttls()
    
      self.__server.login(
        self.__username,
        self.__password
      )

      msg = EmailMessage()
      msg['Subject'] = "Novo livro cadastrado"
      msg['From'] = self.__username
      msg['To'] = self.__list_to_addrs
      msg.set_content(f'\nRespeitosamente;\n\n\nTime de soluções e avisos da FAMIA CORPORATION\nUm novo livro "{self.__book_name}" está disponível, caso tenha interesse, acesse a plataforma e pegue-o emprestado!')

      self.__server.send_message(msg)

      self.__server.quit()
    except:
      return None
  
  def send_message_available(self):
    try:
      self.__server.ehlo()
      self.__server.starttls()
    
      self.__server.login(
        self.__username,
        self.__password
      )

      msg = EmailMessage()
      msg['Subject'] = "O livro está disponível"
      msg['From'] = self.__username
      msg['To'] = self.__list_to_addrs
      msg.set_content(f'\nRespeitosamente;\n\n\nTime de soluções e avisos da FAMIA CORPORATION\nO livro "{self.__book_name}" que você estava esperando está disponível, você tem 7 dias para pegá-lo empréstado!')

      self.__server.send_message(msg)

      self.__server.quit()
    except:
      return None
  
  def send_message_late(self):
    for email, book in zip(self.__list_to_addrs, self.__book_name):
      try:
        self.__server.ehlo()
        self.__server.starttls()
      
        self.__server.login(
          self.__username,
          self.__password
        )

        msg = EmailMessage()
        msg['Subject'] = "Empréstimo em atraso"
        msg['From'] = self.__username
        msg['To'] = email
        msg.set_content(f'\nRespeitosamente;\n\n\nTime de soluções e avisos da FAMIA CORPORATION\nO seu empréstimo do livro "{book}" está em atraso, vá até a biblioteca para devolver o mesmo o mais rápido possível!')

        self.__server.send_message(msg)

        self.__server.quit()
      except:
        pass
  
  def send_message_seven(self):
    try:
      self.__server.ehlo()
      self.__server.starttls()

      self.__server.login(
          self.__username,
          self.__password
        )

      msg = EmailMessage()
      msg['Subject'] = "Removido da fila de espera"
      msg['From'] = self.__username
      msg['To'] = self.__list_to_addrs
      msg.set_content(f'\nRespeitosamente;\n\n\nTime de soluções e avisos da FAMIA CORPORATION\nVisto que o mesmo não foi buscar o livro "{self.__book_name}" que ficou disponível durante 7 dias, você acabou sendo removido da fila de espera.')

      self.__server.send_message(msg)

      self.__server.quit()
    except:
      pass

  def contact_support(self):
    self.__server.ehlo()
    self.__server.starttls()
    
    self.__server.login(
        self.__username,
        self.__password
      )
    
    msg = EmailMessage()
    msg['Subject'] = "Relatório Diário"
    msg['From'] = self.__username
    msg['To'] = self.__list_to_addrs

    msg_content = "\nRespeitosamente;\n\n\nTime de soluções da FAMIA CORPORATION\nRelatório indicando todos os alunos que estão com devoluções pendentes.\n"
    
    for infos in self.__book_name:
      diference = (datetime.now() - datetime.strptime(infos.get('valid_at'), '%Y-%m-%d %H:%M:%S')).days
      msg_content += f"\nNome: {infos.get('nome')}\nValido até: {infos.get('valid_at')}\nDias de atraso: {diference}\n\n"

    msg.set_content(msg_content)

    self.__server.send_message(msg)
    self.__server.quit()
  
  def report_abuse(self):
    self.__server.ehlo()
    self.__server.starttls()
    
    self.__server.login(
        self.__username,
        self.__password
      )
    
    msg = EmailMessage()
    msg['Subject'] = "Abusos identificados"
    msg['From'] = self.__username
    msg['To'] = self.__list_to_addrs

    msg_content = "\nRespeitosamente;\n\n\nTime de soluções da FAMIA CORPORATION\nRelatório indicando todos os abusos ao sistema que foram cometidos. Observação: Pegar um mesmo livro cinco vezes, repetidamente, configura um abuso ao sistema.\n"

    for infos in self.__book_name:
      msg_content += f"\nNome: {infos.get('nome')}\nLivro: {infos.get('titulo')}\nQuantidade de vezes que pegou emprestado: {infos.get('amount')}\n\n"

    msg.set_content(msg_content)

    self.__server.send_message(msg)
    self.__server.quit()