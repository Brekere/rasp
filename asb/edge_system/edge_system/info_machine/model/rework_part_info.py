from edge_system import db


class ReworkPart(db.Model):
    """
    This class is used to display the information of the OK and NOK rework parts/pieces
    """
    __tablename__ = "rework_parts"
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    working_time = db.Column(db.BigInteger)

    def __init__(self, timestamp, status, working_time):
        self.timestamp = timestamp
        self.status = status
        self.working_time = working_time

    def __repr__(self):
        return '<id Rework Part: {}> \n\t\t ok: {} \n\t\t Time {} ms'.format(self.id, self.status, self.working_time)