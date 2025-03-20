from sqlalchemy import event
from flask_login import UserMixin
from ..app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    score_total = db.Column(db.Integer, nullable=False)
    score_current = db.Column(db.Integer, nullable=False)
    tiles_explored = db.Column(db.Integer, nullable=False)
    last_played_gametick = db.Column(db.Integer, nullable=False)
    score_streak = db.Column(db.Integer, nullable=False)
    score_level = db.Column(db.Integer, nullable=False)
    victories = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.boolen, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    scores = db.relationship('Score', backref='user', cascade='all, delete-orphan')


#@event.listens_for(User.__table__, "after_create")
#def createAdminUser(*args, **kwargs):
#    db.session.add(User(name="admin", password_hash="kissa123", role="admin"))
#    db.session.commit()