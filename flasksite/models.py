"""
This file contains the declarations of the models.
"""

from dataclasses import dataclass
from flasksite import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@dataclass  # dataclass is used to allow for converting objects to JSON in the webservice
class User(db.Model, UserMixin):
    id: int
    username: str
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', email='{self.email}', image_file='{self.image_file}')>"


# TODO: create here your models
