from edge_system import db
from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, DateField, IntegerField, HiddenField, StringField
from wtforms.validators import InputRequired 
from flask_wtf.file import FileField


class Part(db.Model):
    """
    This class is used to display the information of the OK and NOK parts/pieces
    """
    __tablename__ = "parts"
    id = db.Column(db.Integer, primary_key = True)
    namepart = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    OK = db.Column(db.Integer)
    NOK = db.Column(db.Integer)
    working_time = db.Column(db.Integer)
    id_machine = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    file = db.Column(db.String(256))

    def __init__(self, id, namepart, timestamp, OK, NOK, working_time, id_machine, file):
        self.id = id
        self.namepart = namepart
        self.timestamp = timestamp
        self.OK = OK
        self.NOK = NOK
        self.working_time = working_time
        self.id_machine = id_machine
        self.file = file
        

    def __repr__(self):
        return '<Part %r >' % (self.id)

class PartForm(FlaskForm):
    id = IntegerField('Id: ', validators=[InputRequired()])
    namepart = StringField('Nombre: ', validators=[InputRequired()])
    timestamp = DateField('Fecha', validators=[InputRequired()])
    OK = IntegerField('OK: ') #, validators=[InputRequired()]
    NOK = IntegerField('NOK: ')#, validators=[InputRequired()]
    working_time = IntegerField('Tiempo de trabajo')#validators=[InputRequired()]
    id_machine = SelectField('Identificador de la maquina: ', coerce=int)
    file = FileField('Archivo')

    
