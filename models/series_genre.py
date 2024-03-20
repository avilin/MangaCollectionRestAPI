from db import db


class SeriesGenreModel(db.Model):
    __tablename__ = "series_genre"

    id = db.Column(db.Integer, primary_key = True)

    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete = "CASCADE"))
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id", ondelete = "CASCADE"))
    
    series = db.relationship("SeriesModel", back_populates = "genres")
    genre = db.relationship("GenreModel", back_populates = "series_list")

    def __init__(self, series_id, genre_id):
        self.series_id = series_id
        self.genre_id = genre_id