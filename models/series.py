from db import db


class SeriesModel(db.Model):
    __tablename__ = "series"

    # id always exists because it comes from MangaUpdates
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    title = db.Column(db.String, nullable = False, unique = True)
    type = db.Column(db.String)
    description = db.Column(db.String)
    image_url = db.Column(db.String)
    status = db.Column(db.String)
    completed = db.Column(db.Boolean)
    anime_start = db.Column(db.String)
    anime_end = db.Column(db.String)
    url = db.Column(db.String)

    authors = db.relationship("SeriesAuthorModel", back_populates = "series", cascade = "all, delete")
    genres = db.relationship("SeriesGenreModel", back_populates = "series", cascade = "all, delete")

    def __init__(self, id, title, type = None, description = None, image_url = None, status = None, completed = None, anime_start = None, anime_end = None, url = None):
        self.id = id
        self.title = title
        self.type = type
        self.description = description
        self.image_url = image_url
        self.status = status
        self.completed = completed
        self.anime_start = anime_start
        self.anime_end = anime_end
        self.url = url