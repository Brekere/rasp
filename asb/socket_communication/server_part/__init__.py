from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig 

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

#from server_part.model.part_info import Part

## create the database 
db.create_all()