from ..app import db

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    attempt = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    scores = db.relationship('Score', backref='level', cascade='all, delete-orphan')