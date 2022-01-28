import email
from flask import jsonify, render_template, request, session
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from datetime import datetime, timedelta
import os
from app.utils import hash_data

from app import app
from app.database.connection import get_db
from app.middlewares import login_required, is_adm

from app.utils.multithreads import Th

from app.services.emailservice import EmailService

from app.models.user import User, user_schema, users_schema
from app.models.book import Book, book_schema, books_schema
from app.models.lending import Lending
from app.models.devolution import Devolution

from app.controllers.UserController import UserController
from app.controllers.BookController import BookController
from app.controllers.AccessController import AccessController
from app.controllers.LendingController import LendingController
from app.controllers.AwaitingController import AwaitingController
from app.controllers.DevolutionController import DevolutionController

@app.route('/')
def home():
  # Criando uma instancia do controlador de emprestimos
  bookcontroller = BookController(get_db())

  LendingPerBooks = bookcontroller.get_books_per_lending_date()

  BooksPerDate = bookcontroller.get_books_per_date_created()

  BooksPerDevolutionDate = bookcontroller.get_books_per_devolution_date()

  return render_template("dashboard.html", LendingPerBooks=LendingPerBooks, BooksPerDate = BooksPerDate, BooksPerDevolutionDate = BooksPerDevolutionDate)


@app.route('/cadastro/', methods=['POST','GET',])
def cadastro():
  if( request.method == "POST" ):
    # Captando as informações enviadas pelo usuario
    nome = request.form.get('nome')
    senha = request.form.get("senha")
    email = request.form.get("email")
    phone = request.form.get("phone")

    # Instanciando o controlador de usuarios
    usercontroller = UserController(get_db())

    # Criando uma instancia de usuario
    user_instance = User(
      nome=nome,
      email=email,
      phone=phone,
      password=hash_data(senha),
      nv_acess= 0
      )
    # Procurando no banco por um usuario especifico
    user_id = usercontroller.create_user( user_instance )
    return redirect(url_for('home'))
  return render_template('cadastro.html')
    
@app.route('/login/',methods=['POST','GET',])
def login():
  if( request.method == "POST" ):
    email = request.form.get('email')
    senha = request.form.get('senha')

    usercontroller = UserController(get_db())

    user_id = usercontroller.autenticar(email=email, senha=hash_data(senha))

    if( user_id is not None ):
      # Salvando os dados do usuario na sessao

      session['logged'] = True 

      session['data'] = {
      'id': user_id['id'],
      'nome': user_id['nome'],
      'phone': user_id['phone'],
      'nv_acess': user_id['nv_acess']}
    else:
      return redirect(url_for('login'))
  
    return redirect(url_for('home'))
  
  return render_template('login.html')



@app.route('/confirm-get-awaiting/', methods=['GET',])
@login_required
@is_adm
def all_awaiting():
  # Criando uma instancia do controlador de livros
  bookcontroller = BookController(get_db())

  # Captando os livros que foram recentemente devolvidos e possuem pessoas na fila de espera
  books = bookcontroller.get_books_awaiting()

  await_list = []

  # Se existir os livros
  if( len(books) > 0 ):
    # Criando uma instancia do controlador da fila de espera
    awaitingcontroller = AwaitingController(get_db())

    # Percorrendo todos os livros que estao contidos nas filas de espera
    for book in books:
      infos = awaitingcontroller.verify_awaiting_list_per_book(book['book_id'])
      
      if( len( infos ) > 0 ):
        await_list.append(infos[0])
  
  return render_template('confirmawait.html', awaiting_list=await_list)

@app.route('/validate-await-lending/<awaiting_id>/', methods=['GET',])
@login_required
@is_adm
def validate_await_lending(awaiting_id: int):
  # Criando uma instancia do controlador de fila de espera
  awaitingcontroller = AwaitingController(get_db())

  # Captando as informacoes de uma posicao da fila especifica
  await_info = awaitingcontroller.obter(awaiting_id)

  if( await_info is not None ):
    # Criando uma instancia do controlador de emprestimos
    lendingcontroller = LendingController(get_db())

    # Instanciando um emprestimo
    lending = Lending(
      user_id=await_info.get('user_id'),
      book_id=await_info.get('book_id')
    )

    # Criando um emprestimo
    lending_id = lendingcontroller.create_lending(lending)

    # Verificando se foi possivel fazer o registro com sucesso
    if( lending_id > 0 ):
      # Removendo o usuario da lista de espera
      n_deletados = awaitingcontroller.delete(awaiting_id)

      if( n_deletados > 0 ):
        flash('Empréstimo validado com sucesso.', 'success')
        return redirect(url_for('all_awaiting'))
      else:
        flash('Houve um erro ao tentar retirar o usuário da fila de espera, entre em contato com o suporte!', 'danger')
        return redirect(url_for('all_awaiting'))

    else:
      flash('Ocorreu um erro ao tentar acessar a funcionalidade, entre em contato com o suporte!', 'danger')
      return redirect(url_for('all_awaiting'))

  else:
    flash('Não existe uma pessoa na fila que possua essa posição.', 'warning')
    return redirect(url_for('all_awaiting'))


@app.route("/books/", methods=['GET',])
@login_required
def list_all_books():
  # Instanciando o controlador de livros
  bookcontroller = BookController(get_db())

  books = bookcontroller.get_all() # Pegando todos os livros que foram cadastrados

  return render_template("booklist.html", books = books)

@app.route("/books/create/", methods=['GET', 'POST',])
@login_required
def create_book():
  if( request.method == "POST" ):
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    autor = request.form.get('autor')
    ano_lancamento = request.form.get('ano_lancamento')
    arquivo = request.files.get('arquivo')
    momento = str(datetime.today().timestamp()).replace('.', '')
    
    if( session.get('data', None) ):
      if( titulo and arquivo ):
        # Instanciando o controlador de livros
        bookcontroller = BookController(get_db())

        caminho_imagem = f"{momento}{arquivo.filename}"

        # Criando uma instancia de livro
        book = Book(
          titulo=titulo,
          descricao=descricao,
          autor=autor,
          ano_lancamento=ano_lancamento,
          caminho_imagem=caminho_imagem,
          user_id=session['data']['id']
        )

        try:
          book_id = bookcontroller.create_book( book )
          arquivo.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), caminho_imagem))
        except os.error as err:
          print(err)
          flash("Ocorreu um erro ao tentar registrar o livro", "danger") # 400 - Bad Request
          return redirect(request.url)

        if( book_id is not None ):
          try: # Tentando enviar emails para todos os usuários existentes no sistema
            list_to_addrs = list(map(lambda x: x.get('email'), UserController(get_db()).get_all_emails()))
  
            emailservice = EmailService(
              username=os.environ.get('FROM'), 
              password=os.environ.get('PASS'),
              list_to_addrs=list_to_addrs,
              book_name=""
            )

            emailservice.set_book_name(book.titulo)
            Th(num=1, func=emailservice.send_message_new_book).start()
          except:
            pass

          flash("Livro cadastrado com sucesso!", "success") # 201 - Created
          return redirect(request.url)

        flash("Não foi possível registrar o livro, tente novamente!", "danger") # 400 - Bad Request
        return redirect(request.url)
        
      else:
        flash("Preencha todos os campos!", "warning") # 422 - Unprocessable Entity
    
    else:
      flash("É necessário estar logado para ter acesso a essa funcionalidade!", "danger") # 401 - Unauthorized
      return redirect(url_for("login"))
  
  return render_template("democreatebook.html")

@app.route("/books/update/<book_id>/", methods=['GET', 'POST',])
@login_required
def update_book(book_id: int):
  # Instanciando o controlador de livros
  bookcontroller = BookController(get_db())

  if( request.method == "POST" ):
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    autor = request.form.get('autor')
    ano_lancamento = request.form.get('ano_lancamento')

    if( titulo ):
      book_id = bookcontroller.get_one(book_id)

      if( book_id is not None ):
        book = Book(
          titulo=titulo,
          descricao=descricao,
          autor=autor,
          ano_lancamento=ano_lancamento,
          caminho_imagem="",
          user_id=0
        )

        book.id = book_id['id']

        n_updates = bookcontroller.update_book(book)

        if( n_updates > 0 ):
          flash("Informações do livro atualizadas com sucesso!", 'success'), 200
        else:
          flash("Nenhuma alteração foi feita!", 'warning'), 400
      
        return redirect(url_for('list_all_books'))
      else:
        flash("O livro tal qual deseja editar não existe!", 'danger'), 400
        return redirect(url_for('list_all_books'))
    else:
      flash("Preencha todos os campos!", 'warning') # 422 - Unprocessable Entity
      return redirect(url_for('list_all_books'))
    
  else:
    book = bookcontroller.get_one(book_id)

    if( book is not None ):
      return render_template("democreatebook.html", book_info=book, edit=True)
    else:
      flash("O livro tal qual deseja editar não existe!", 'warning'), 400
      return redirect(url_for('list_all_books'))

@app.route("/books/delete/<book_id>/", methods=['GET',])
@login_required
def delete_book(book_id):
  # Criando uma instancia do controlador de emprestimos
  lendingcontroller = LendingController(get_db())

  # Criando uma instancia do controlador de livros
  bookcontroller = BookController(get_db())

  # Pegando um determinado livro por seu id
  book = bookcontroller.get_one(book_id)

  # Verificando se o livro existe
  if( book is not None ):
    exists_lending = lendingcontroller.verify_lending_book(book_id)

    # Verificando se um determinado livro esta emprestado a alguem
    if( exists_lending is None ):
      n_deleted = bookcontroller.delete_book(book_id)

      if( n_deleted > 0 ):
        flash(f"Livro apagado com sucesso!", "success"), 200
        return redirect(url_for("list_all_books"))
      
      else:
        flash(f"Não foi possíel apagar o livro, entre em contato com o suporte!", "danger"), 400
        return redirect(url_for("list_all_books"))
    else:
      flash(f"Não foi possível apagar o livro pois o mesmo está empréstado a alguém!", "warning"), 400
      return redirect(url_for("list_all_books"))
  else:
    flash(f"O livro que desejas apagar não existe!", "danger"), 400
    return redirect(url_for("list_all_books"))

@app.route("/books/search", methods=['GET',])
@login_required
def search_books():
  # Pegando o parametro "title" que foi passado pela url
  title = request.args.get('title')

  # Instanciando o controlador de livros
  bookcontroller = BookController(get_db())

  # Pegando todos os livros que tenham a palavra chave que foi passado via url em seu titulo
  books = bookcontroller.search_book(title)

  return render_template("booklist.html", books = books)

@app.route('/books/give-back/<lending_id>/', methods=['GET',])
@login_required
def give_back(lending_id: int):
  # Criando uma instancia do controlador de emprestimos
  lendingcontroller = LendingController(get_db())

  # Criando uma instancia do controlador de lista de espera
  awaitingcontroller = AwaitingController(get_db())

  # Captando um emprestimo no banco
  lending = lendingcontroller.get_one(lending_id)

  # Verificando se existe um emprestimo
  if( lending is not None ):
    # Verificando se o usuario que pegou o livro emprestado eh o usuario que esta logado atualmente
    if( lending.get('user_id') == session['data'].get('id') ):
      # Criando uma instancia do controlador de devolucoes
      devolutioncontroller = DevolutionController(get_db())

      # Criando uma instancia de devolucao
      devolution = Devolution(lending_id=lending.get('id'))

      devolution_id = devolutioncontroller.register_devolution(devolution)

      if( devolution_id > 0 ):
        # Procurando pessoas na lista de espera pelo livro
        awaiting_list = awaitingcontroller.verify_awaiting_list_per_book(lending.get('book_id'))

        # Verificando se existem pessoas na fila de espera
        if( len(awaiting_list) > 0 ):
          try: # Tentando enviar emails para todos os usuários existentes no sistema
            emailservice = EmailService(
              username=os.environ.get('FROM'), 
              password=os.environ.get('PASS'),
              list_to_addrs=awaiting_list[0].get('email'),
              book_name=lending.get('titulo')
            )

            Th(num=1, func=emailservice.send_message_available).start()
          except:
            pass

        flash("O livro foi devolvido com sucesso!", 'success')
        return redirect(url_for('list_all_books'))

      flash("Não foi possível fazer a devolução do livro, tente novamente", 'danger')
      return redirect(url_for('list_all_books'))

    flash("Não é possível fazer a devolução de um livro que não foi emprestado a você!", 'warning'), 400
    return redirect(url_for('list_all_books'))

  flash("Não foi possível declarar a devolução do livro pois esse empréstimo já foi declarado anteriormente como devolvido!", 'warning'), 400
  return redirect(url_for('list_all_books'))
    
    

@app.route("/books/renew/<lending_id>/", methods=['GET',])
@login_required
def renew_book(lending_id: int):
  # Criando uma instancia do controlador de emprestimos
  lendingcontroller = LendingController(get_db())

  # Criando uma instancia do controlador de lista de espera
  awaitingcontroller = AwaitingController(get_db())

  # Captando um emprestimo no banco
  lending = lendingcontroller.get_one(lending_id)

  # Verificando se existe um emprestimo
  if( lending is not None ):
    # Procurando pessoas na lista de espera pelo livro
    awaiting_list = awaitingcontroller.verify_awaiting_list_per_book(lending.get('book_id'))

    # Verificando se existem pessoas na fila de espera
    if( len(awaiting_list) == 0 ):
      # Verificando se o usuario que pegou o livro emprestado eh o usuario que esta logado atualmente
      if( lending.get('user_id') == session['data'].get('id') ):
        
        validade = datetime.strptime(lending.get('valid_at'), '%Y-%m-%d %H:%M:%S')
        data_atual = datetime.now()
        intervalo = timedelta(days=3)

        if( (validade - data_atual) > intervalo  ):
          flash('Só é possível renovar 3 dias antes da data de validade.', 'warning')
          return redirect(url_for('list_my_lendings'))
          

        # Criando uma instancia do controlador de devolucoes
        devolutioncontroller = DevolutionController(get_db())

        # Criando uma instancia de devolucao
        devolution = Devolution(lending_id=lending.get('id'), renew=True)

        try:
          lending_instance = Lending(user_id=session['data'].get('id'), book_id=lending.get('book_id'))
          
          devolution_id = devolutioncontroller.register_devolution(devolution)
          renew_id = lendingcontroller.create_lending(lending_instance)

          if( renew_id is not None ):
            flash("Renovação efetuada com sucesso!", 'success'), 201
            return redirect(url_for('list_all_books'))
          else:
            flash("Houve um problema ao tentar renovar o empréstimo, tente novamente, caso o problema volte a se repetir, entre em contato com o suporte!", 'danger'), 400
            return redirect(url_for('list_all_books'))

        except:
          flash("Houve um problema ao tentar renovar o empréstimo, entre em contato com o suporte!", 'danger'), 400
          return redirect(url_for('list_all_books'))

      else:
        flash("Não é possível renovar um empréstimo de outra pessoa!", 'warning'), 400
        return redirect(url_for('list_all_books'))
    else:
      flash("Não foi possível renovar o empréstimo visto que existem pessoas na fila de espera por esse livro!", 'warning'), 400
      return redirect(url_for('list_all_books'))

  else:
    flash("Não existe empréstimo registrado com esse ID!", 'warning'), 400
    return redirect(url_for('list_all_books'))

@app.route("/books/detail/<book_id>/", methods=['GET',])
@login_required
def detail_book(book_id: int):

  bookcontroller = BookController(get_db())
  usercontroller = UserController(get_db())

  book = bookcontroller.get_one(book_id)
  user = usercontroller.get_one(book['user_id'])

  return render_template("bookdetails.html", book = book, user = user)

@app.route("/lending/<book_id>/", methods=['GET',])
@login_required
def view_lending_book(book_id: int):
  # Criando uma instancia do controlador de emprestimos
  lendingcontroller = LendingController(get_db())

  lendings = lendingcontroller.get_all_per_book(book_id)

  return jsonify(lendings=lendings)

@app.route("/books/lending/<book_id>/", methods=['GET', 'POST',])
@login_required
def lending_book(book_id: int):
  # Criando uma instancia do controlador de emprestimos
  lendingcontroller = LendingController(get_db())

  # Criando uma instancia do controlador de lista de espera
  awaitingcontroller = AwaitingController(get_db())

  exists_lending = lendingcontroller.verify_lending_book(book_id)
  awaiting_list = awaitingcontroller.verify_awaiting_list_per_book(book_id)

  lending = Lending(
    user_id=session['data']['id'],
    book_id=book_id
  )

  # Se nenhuma pessoa estiver com esse livro emprestado e não haver ninguem na fila de espera por ele
  if( exists_lending == None and len(awaiting_list) == 0 ):
    # Registrando o emprestimo no banco
    lending_id = lendingcontroller.create_lending(lending)

    # Se foi possivel registrar o emprestimo
    if( lending_id is not None ):
      flash(f"Empréstimo efetuado com sucesso! Você já pode ir até a biblioteca buscar o livro!", "success"), 201
    else:
      flash(f"Houve um erro ao tentar pegar o livro emprestado, entre em contato com o suporte!", "danger"), 400

    return redirect(url_for("list_my_lendings"))

  # Se existir pessoas na fila de espera
  elif( len(awaiting_list) > 0 ):
    if( exists_lending ):
      if( exists_lending.get('user_id') == session['data']['id'] ):
        flash(f"Não foi possível lhe adicionar a lista de espera pois o livro está com você!","warning"), 400
        return redirect(url_for("list_my_lendings"))

    # Verificando se o usuario ja esta na lista de espera
    if( session['data']['id'] in list(map( lambda x: x.get('id') if x.get('id') == session['data']['id'] else None, awaiting_list )) ):
      flash(f"Não foi possível lhe adicionar a fila de espera pois você já está contido nela!","warning"), 400
      return redirect(url_for('awaiting_list', book_id = book_id))

    # Captando a fila de espera de um determinado livro
    in_await = awaitingcontroller.verify_awaiting_list_per_book(book_id)

    # Verificando se o usuario ja esta na fila de espera
    if( session['data']['id'] in list(map(lambda x: x.get('user_id'), in_await)) ):
      flash('Não foi possível lhe adicionar a fila de espera pois você já está contido nela!', 'warning')
      return redirect(url_for('awaiting_list', book_id = book_id))

    # Colocando o usuario na fila de espera pelo livro
    awaiting_id = awaitingcontroller.create_awaiting_list( awaiting=lending )

    # Se foi possivel registrar o usuario na fila
    if( awaiting_id is not None ):
      flash("Você foi adicionado a fila de espera!", "success"), 201
      return redirect(url_for('awaiting_list', book_id = book_id))

    flash(f"Houve um erro ao tentar entrar na fila de espera, entre em contato com o suporte!","danger"), 400
    return redirect(url_for("list_all_books"))
  
  # Se o livro tiver emprestado a alguem
  if( exists_lending ):
    if( exists_lending.get('user_id') == session['data']['id'] ):
      flash(f"Não foi possível lhe adicionar a lista de espera pois o livro está com você!","warning"), 400
      return redirect(url_for("list_my_lendings"))

    # Colocando o usuario na fila de espera pelo livro
    awaiting_id = awaitingcontroller.create_awaiting_list( awaiting=lending )

    # Se foi possivel registrar o usuario na fila
    if( awaiting_id is not None ):
      flash("Você foi adicionado a fila de espera!", "success"), 201
      return redirect(url_for('awaiting_list', book_id = book_id))

    flash(f"Houve um erro ao tentar entrar na fila de espera, entre em contato com o suporte!","danger"), 400
    return redirect(url_for("list_all_books"))

@app.route('/devolutions/me/')
@login_required
def list_my_devolutions():
  # Instanciando o controlador de devolucoes
  devolutioncontroller = DevolutionController(get_db())

  # Captando todas as devolucoes do usuario
  list_devolutions = devolutioncontroller.get_my_devolutions(session['data'].get('id'))

  print(list_devolutions)

  return render_template('devolutionlist.html', devolutions = list_devolutions)

@app.route('/lendings/me/')
@login_required
def list_my_lendings():
  # Instanciando o controlador de devolucoes
  lendingcontroller = LendingController(get_db())

  # Captando todas as devolucoes do usuario
  list_lendings = lendingcontroller.get_my_lendings(session['data'].get('id'))
  

  return render_template('lendinglist.html', lendings=list_lendings)

@app.route('/awaiting/<book_id>/')
@login_required
def awaiting_list(book_id: int):
  # Instanciando o controlador da fila de espera
  awaitingcontroller = AwaitingController(get_db())

  bookcontroller = BookController(get_db())

  awaiting = awaitingcontroller.verify_awaiting_list_per_book(book_id)

  if( len(awaiting) == 0):
    flash('Não existe ninguém na fila de espera!', 'warning')
    return redirect(url_for('list_all_books'))

  book = bookcontroller.get_one(awaiting[0]['book_id'])

  return render_template("awaitlist.html", awaiting = awaiting, book = book)

@app.route("/logout/")
@login_required
def logout():
  # Limpando a sessão apagando tudo que foi armazenado na mesma
  session['data'] = None
  session.clear()

  # Retornando uma mensagem para informar o usuario que a operação foi efetuada com sucesso
  flash(f"Logout feito com sucesso", "success")

  return redirect(url_for("login")) # Redirecionando o usuario para a tela de login

@app.route('/verify/late/', methods=['GET',])
def verify():
  # Criando uma instancia do controlador de emprestimos
  lendingcontroller = LendingController(get_db())

  # Captando todos os emprestimos em atraso
  late = lendingcontroller.get_all_late_lendings()

  # Verificando se existe algum emprestimo atrasado
  if( len(late) > 0):
    # Captando o email de todos os usuarios com emprestimos pendentes
    emails = list(map(lambda x: x.get('email'), late))
    
    # Captando os livros pendentes 
    livros = list(map(lambda x: x.get('titulo'), late))
    
    # Criando uma instancia do servico de email
    emailservice = EmailService(
      username=os.environ.get('FROM'), 
      password=os.environ.get('PASS'),
      list_to_addrs=emails,
      book_name=livros
    )
    
    # Executando uma funcao em uma thread especifica
    Th(num=3, func=emailservice.send_message_late).start()

    # Criando uma instancia do servico de email
    emailservice = EmailService(
      username=os.environ.get('FROM'), 
      password=os.environ.get('PASS'),
      list_to_addrs=['fizzanimal@gmail.com'],
      book_name=late
    )

    Th(num=1, func=emailservice.contact_support).start()

  return jsonify(late)

@app.route('/verify/devolution-seven/', methods=['GET',])
def verify_seven():
  # Criando uma instancia do controlador de livros
  bookcontroller = BookController(get_db())

  # Captando os livros que foram recentemente devolvidos e possume pessoas na fila de espera
  books = bookcontroller.get_books_awaiting()

  # Se existir os livros
  if( len(books) > 0 ):
    # Criando uma instancia do controlador da fila de espera
    awaitingcontroller = AwaitingController(get_db())
  
    for book in books:
      infos = awaitingcontroller.verify_awaiting_list_per_book(book['book_id'])

      if( len(infos) > 0 ):
        data_devolucao = datetime.strptime(book.get('data'), '%Y-%m-%d %H:%M:%S')
        data_atual = datetime.now()

        if( (data_atual - data_devolucao).days % 7 == 0 ):
          n_deletados = awaitingcontroller.delete(infos[0].get('id'))          

          if( n_deletados > 0 ):
            emailservice = EmailService(
              username=os.environ.get('FROM'), 
              password=os.environ.get('PASS'),
              list_to_addrs=infos[0].get('email'),
              book_name=infos[0].get('titulo')
            )

            Th(num=1, func=emailservice.send_message_seven).start()
  
  return 'Nice'

@app.route('/verify/abuses/', methods=['GET',])
def report_abuse():
  # Criando uma instancia do controlador de emprestimos
  lendingcontroller = LendingController(get_db())

  # Captando os abusos ao sistema
  abuses = lendingcontroller.get_abuses()

  # Verificando se existem abusos
  if( len(abuses) > 0 ):
    emailservice = EmailService(
      username=os.environ.get('FROM'), 
      password=os.environ.get('PASS'),
      list_to_addrs=['fizzanimal@gmail.com'],
      book_name=abuses
    )

    Th(num=2, func=emailservice.report_abuse).start()
  
  return 'Nice'

@app.route('/about/', methods=['GET',]) 
def about():

  bookcontroller = BookController(get_db())
  lendingcontroller = LendingController(get_db())
  usercontroller = UserController(get_db())

  books = bookcontroller.get_count_all()
  lendings = lendingcontroller.get_count_all()
  users = usercontroller.get_count_all()


  return render_template("about.html", books = books, lendings = lendings, users=users)    

@app.route('/adm/panel', methods=['GET',])
@is_adm
def adm_panel():

  lendingcontroller = LendingController(get_db())

  lendingspermonth = lendingcontroller.get_lendings_per_month()

  peoplesservedpermonth = lendingcontroller.people_served()

  bookcontroller = BookController(get_db())

  bookspermonth = bookcontroller.get_books_per_month()

  return render_template("admpanel.html", lendingspermonth = lendingspermonth, bookspermonth = bookspermonth, peoplesservedpermonth = peoplesservedpermonth)

@app.route('/books/historic/<book_id>/', methods=['GET',])
@login_required
def book_historic(book_id: int):

  lendingcontroller = LendingController(get_db())

  bookhistoric = lendingcontroller.get_all_per_book(book_id)

  bookcontroller = BookController(get_db())

  book = bookcontroller.get_one(book_id)

  return render_template('bookhistoric.html', bookhistoric = bookhistoric, book = book)
