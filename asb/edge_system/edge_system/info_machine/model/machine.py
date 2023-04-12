from edge_system import db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, DecimalField, HiddenField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired


class Machine(db.Model):
    """
    Class tha contain the information of the machine (For local database ...)
    """
    __tablename__ = "machines"
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(45))
    description = db.Column(db.String(256))
    brand = db.Column(db.String(64))
    model = db.Column(db.String(64))
    voltage = db.Column(db.Integer)
    amperage = db.Column(db.Float)
    serie = db.Column(db.String(45))
    id_line = db.Column(db.Integer) # en la base de datos lo tengo como string, cambiar esto a un entero en la base de datos
    manufacturing_date = db.Column(db.DateTime)
    instalation_date = db.Column(db.DateTime)
    id_supplier = db.Column(db.Integer)
    run_date = db.Column(db.DateTime)
    file = db.Column(db.String(256))
    parts = db.relationship('Part', backref='machine', lazy='select')

    def __init__(self, id, nickname, description, brand, model, voltage, amperage, serie, id_line, manufacturing_date, 
    instalation_date, id_supplier, run_date, file):
        self.id = id
        self.nickname = nickname
        self.description = description
        self.brand = brand
        self.model = model
        self.voltage = voltage
        self.amperage = amperage
        self.serie = serie
        self.id_line = id_line
        self.manufacturing_date = manufacturing_date
        self.instalation_date = instalation_date
        self.id_supplier = id_supplier
        self.run_date = run_date
        self.file = file

    def __repr__(self):
        return '<Machine: {}>'.format(self.nickname)

class RegisterForm(FlaskForm):
    id = IntegerField('Id', validators = [InputRequired()])
    nickname = StringField('Nickname', validators = [InputRequired()])
    description = StringField('Description', validators = [InputRequired()])
    brand = StringField('Brand', validators = [InputRequired()])
    model = StringField('Model', validators = [InputRequired()])
    voltage = DecimalField('Voltage', validators = [InputRequired()])
    amperage = StringField('Amperage', validators = [InputRequired()])
    serie = StringField('Serie', validators = [InputRequired()])
    id_line = IntegerField('Line id', validators = [InputRequired()])
    manufacturing_date = DateField('Manufacturing date', validators = [InputRequired()])
    instalation_date = DateField('Instalation date', validators = [InputRequired()])
    id_supplier = IntegerField('Supplier id', validators = [InputRequired()])
    run_date = DateField('Run date', validators = [InputRequired()])
    file = FileField('Archivo') #, validators = [FileRequired()]
    