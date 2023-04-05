from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_socketio import SocketIO

app = Flask(__name__)

## Database configuration ... 

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://agg:db.#As4kL@localhost:3306/historic"

app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)
# PostgreSQL: postgresql+psycopg2://user:password@ip:port/db_name
#socketio = SocketIO(app)

## import views
from edge_system.info_machine.views import machine
from edge_system.home.views import home

app.register_blueprint(machine)
app.register_blueprint(home)


## create the database 
with app.app_context():
    db.create_all()