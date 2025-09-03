from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='User')

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.role = 'User'

    def __str__(self):
        return f'{self.username}'
