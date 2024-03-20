from db import db


class SeriesAuthorModel(db.Model):
    __tablename__ = "series_author"

    id = db.Column(db.Integer, primary_key = True)

    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete = "CASCADE"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id", ondelete = "CASCADE"))
    
    type = db.Column(db.String(80), nullable = False)
    
    series = db.relationship("SeriesModel", back_populates = "authors")
    author = db.relationship("AuthorModel", back_populates = "series_list")

    def __init__(self, series_id, author_id, type):
        self.series_id = series_id
        self.author_id = author_id
        self.type = type