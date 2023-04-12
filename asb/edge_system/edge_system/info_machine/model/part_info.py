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
    status = db.Column(db.String(255))
    working_time = db.Column(db.Integer)
    id_machine = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False) #db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


    def __init__(self, id, namepart, timestamp, status, working_time, id_machine):
        self.id = id
        self.namepart = namepart
        self.timestamp = timestamp
        self.status = status
        self.working_time = working_time
        self.id_machine = id_machine
        

    def __repr__(self):
        return '<Part %r >' % (self.id)

class PartForm(FlaskForm):
    id = IntegerField('Id: ', validators=[InputRequired()])
    namepart = StringField('Nombre: ', validators=[InputRequired()])
    timestamp = DateField('Fecha', validators=[InputRequired()])
    status = StringField('Status: ', validators=[InputRequired()])
    working_time = IntegerField('Tiempo de trabajo', validators=[InputRequired()])
    id_machine = SelectField('Maquina: ', coerce=int)

    
