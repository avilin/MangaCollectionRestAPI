from db import db


class UserSeriesModel(db.Model):
    __tablename__ = "user_series"

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = "CASCADE"))
    series_id = db.Column(db.Integer, db.ForeignKey("series.id", ondelete = "CASCADE"))

    rating = db.Column(db.Integer)
    review = db.Column(db.String)
    volumes_expected = db.Column(db.Integer, nullable = False)
    timestamp = db.Column(db.Double)
    private = db.Column(db.Boolean)
    
    user = db.relationship("UserModel", back_populates = "series_list")
    series = db.relationship("SeriesModel", back_populates = "users")

    def __init__(self, user_id, series_id, rating = None, review = None, volumes_expected = None, timestamp = None, private = True):
        self.user_id = user_id
        self.series_id = series_id
        self.rating = rating
        self.review = review
        self.volumes_expected = volumes_expected
        self.timestamp = timestamp
        self.private = private