from ..app import db

class TurnCounter(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    counter = db.Column(db.Integer, unique=True)