from db import db


class EditionModel(db.Model):
    __tablename__ = "edition"

    id = db.Column(db.Integer, primary_key = True)
    
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete = "CASCADE"))
    editorial_id = db.Column(db.Integer, db.ForeignKey("editorial.id", ondelete = "CASCADE"))

    format = db.Column(db.String(80), nullable = False) # Use as id to avoid duplicates
    volumes = db.Column(db.Integer, nullable = False)
    discontinued = db.Column(db.Boolean, nullable = False)
    size = db.Column(db.String(80))

    editorial = db.relationship("EditorialModel", back_populates = "editions")
    series = db.relationship("SeriesModel", back_populates = "editions")
    users = db.relationship("UserEditionModel", back_populates = "edition")

    def __init__(self, series_id, editorial_id, format, volumes = 0, discontinued = False, size = None):
        self.series_id = series_id
        self.editorial_id = editorial_id
        self.format = format
        self.volumes = volumes
        self.discontinued = discontinued
        self.size = size