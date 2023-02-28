from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user

app = Flask(__name__)

## Database configuration ... 

app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)

# manejo de logoin .... 
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "fauth.login"

# para cuando un administrador entre para el manejo de usuarios ... 
#def role_admin_need(f):
#   @wraps(f)
#   def wrapper(*args, **kwds):
#      if current_user.rol.value != "admin":
#         logout_user()
#         return redirect(url_for('fauth.login'))
#      return f(*args, **kwds)
#   return wrapper


## import views
from edge_system.info_machine.views import machine
from edge_system.home.views import home
from edge_system.fauth.login_controller import fauth

app.register_blueprint(machine)
app.register_blueprint(home)
app.register_blueprint(fauth)


## create the database 
db.create_all()