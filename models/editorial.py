from db import db
from enum import Enum


class Language(str, Enum):
    ES = "ES",
    EN = "EN",
    JP = "JP"


class EditorialModel(db.Model):
    __tablename__ = "editorial"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False, unique = True)
    language = db.Column(db.Enum(Language, create_constraint=True, validate_strings=True,), nullable = False)

    editions = db.relationship("EditionModel", back_populates = "editorial", cascade = "all, delete")

    def __init__(self, name, language = "ES"):
        self.name = name
        self.language = language