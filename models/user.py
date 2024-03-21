from db import db
from enum import Enum
import bcrypt


class Rights(str, Enum):
    SUPERADMIN = "SUPERADMIN",
    ADMIN = "ADMIN",
    USER = "USER"


class UserModel(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key = True)
    
    email = db.Column(db.String(80), nullable = False, unique = True)
    username = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    rights = db.Column(db.Enum(Rights, create_constraint=True, validate_strings=True,), nullable = False)

    series_list = db.relationship("UserSeriesModel", back_populates = "user", cascade = "all, delete")

    def __init__(self, email, username, password, rights = "USER"):
        self.email = email
        self.username = username
        self.password = bcrypt.hashpw(
            password = password.encode('utf-8'),
            salt = bytes(bcrypt.gensalt())
        )
        self.rights = rights

    def check_password(self, password):
        return bcrypt.checkpw(
            password = password.encode('utf-8'),
            hashed_password = self.password
        )
    
    def update_password(self, password):
        self.password = bcrypt.hashpw(
            password = password.encode('utf-8'),
            salt = bytes(bcrypt.gensalt())
        )