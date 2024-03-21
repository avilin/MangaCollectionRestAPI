from db import db
from enum import Enum


class Format(str, Enum):
    TANKOUBON = "Tankoubon",
    OMNIBUS = "Omnibus",
    THREEINONE = "3 in 1",
    DIGITAL = "Digital"


class EditionModel(db.Model):
    __tablename__ = "edition"

    id = db.Column(db.Integer, primary_key = True)
    
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete = "CASCADE"))
    editorial_id = db.Column(db.Integer, db.ForeignKey("editorial.id", ondelete = "CASCADE"))

    volume_format = db.Column(db.Enum(Format, create_constraint=True, validate_strings=True,), nullable = False) # Use as id to avoid duplicates
    volumes = db.Column(db.Integer, nullable = False)
    discontinued = db.Column(db.Boolean, nullable = False)
    size = db.Column(db.String(80))

    editorial = db.relationship("EditorialModel", back_populates = "editions")
    series = db.relationship("SeriesModel", back_populates = "editions")
    users = db.relationship("UserEditionModel", back_populates = "edition")

    def __init__(self, series_id, editorial_id, volume_format = "Tankoubon", volumes = 0, discontinued = False, size = None):
        self.series_id = series_id
        self.editorial_id = editorial_id
        self.volume_format = volume_format
        self.volumes = volumes
        self.discontinued = discontinued
        self.size = size