from db import db


class GenreModel(db.Model):
    __tablename__ = "genre"
    
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(80), nullable = False, unique = True)

    series_list = db.relationship("SeriesGenreModel", back_populates = "genre", cascade = "all, delete")

    def __init__(self, name):
        self.name = name