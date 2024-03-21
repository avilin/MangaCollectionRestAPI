from db import db


class UserVolumeModel(db.Model):
    __tablename__ = "user_volume"

    id = db.Column(db.Integer, primary_key = True)

    user_edition_id = db.Column(db.Integer, db.ForeignKey("user_edition.id", ondelete = "CASCADE"))

    number = db.Column(db.Integer, nullable = False) # Use as id to avoid duplicates
    price = db.Column(db.Float, nullable = False)
    
    user_edition = db.relationship("UserEditionModel", back_populates = "volumes")

    def __init__(self, user_edition_id, number, price):
        self.user_edition_id = user_edition_id
        self.number = number
        self.price = price