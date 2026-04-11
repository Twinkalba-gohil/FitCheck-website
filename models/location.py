from models import db

class State(db.Model):
    __tablename__ = "state_table"

    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False)


class City(db.Model):
    __tablename__ = "city_table"

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("state_table.state_id"))


