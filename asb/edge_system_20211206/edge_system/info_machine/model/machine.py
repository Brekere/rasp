#from edge_system import db

class Machine():
    """
    Class tha contain the information of the machine 
    """
    def __init__(self, nickname, description, brand, model, voltage, amperage, serie, id_line, manufacturing_date, instalation_date, id_supplier, run_date):
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

    def __repr__(self):
        return '<Machine: {}>'.fromat(self.nickname)