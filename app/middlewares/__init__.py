from functools import wraps
from flask import session, flash
from flask.helpers import url_for
from werkzeug.utils import redirect

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if( session.get('data') is None ):
      flash("É necessário estar logado para ter acesso a essa funcionalidade!", "warning")
      
      return redirect(url_for("login"))
    
    return f(*args, **kwargs)
  
  return decorated_function

def is_adm(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if( session['data'].get('nv_acess') != 1 ):
      flash("Essa funcionalidade é exclusiva para administradores!", 'danger')
      
      return redirect(url_for('home'))
    
    return f(*args, **kwargs)
  
  return decorated_function
