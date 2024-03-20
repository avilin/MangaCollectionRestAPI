from db import db


class AuthorModel(db.Model):
    __tablename__ = "author"
    
    # id always exists because it comes from MangaUpdates
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    
    name = db.Column(db.String(80), nullable = False, unique = True)

    series_list = db.relationship("SeriesAuthorModel", back_populates = "author", cascade = "all, delete")

    def __init__(self, id, name):
        self.id = id
        self.name = name