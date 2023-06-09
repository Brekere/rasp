from edge_system import db
from sqlalchemy import Enum
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, HiddenField, IntegerField
from wtforms.validators import EqualTo, InputRequired
import enum

class RolUser(enum.Enum):
    admin = 'Administrador'
    operador = 'Operador'
    linea = 'Encargado de linea'
    mtto = 'Mantenimiento'

class UsersLogin(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40))
    fullname = db.Column(db.String(256))
    pwhash = db.Column(db.String(256))
    id_employee = db.Column(db.Integer) # va a tener relación con el id
    id_role  = db.Column(Enum(RolUser)) # Operador, encargado de línea o mantenimiento

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, id, username, fullname, pwhash, id_employee, id_role):
        self.id = id
        self.username = username
        self.fullname = fullname
        self.pwhash = generate_password_hash(pwhash)
        self.id_employee = id_employee
        self.id_role = id_role

    def __repr__(self):
        return 'User : %r' % (self.username)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

class RegisterForm(FlaskForm):
    id = IntegerField('id', validators = [InputRequired()])
    username = StringField('User', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    fullname = StringField('Full name', validators = [InputRequired()])
    id_employee = IntegerField('Employee id', validators = [InputRequired()])
    id_role  = StringField('Role id', validators = [InputRequired()])
    confirm  = PasswordField('Repeat password')


class LoginForm(FlaskForm):
    username = StringField('User', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    next = HiddenField('next')