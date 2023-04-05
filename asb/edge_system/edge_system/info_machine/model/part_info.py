from edge_system import db


class Part(db.Model):
    """
    This class is used to display the information of the OK and NOK parts/pieces
    """
    __tablename__ = "parts"
    id = db.Column(db.Integer, primary_key = True)
    id_machine = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    working_time = db.Column(db.BigInteger)

    def __init__(self, id_machine, timestamp, status, working_time):
        self.id_machine = id_machine
        self.timestamp = timestamp
        self.status = status
        self.working_time = working_time

    def __repr__(self):
        return '<id Machine: {}> \n\t\t ok: {} \n\t\t Time {} ms'.format(self.id_machine, self.status, self.working_time)