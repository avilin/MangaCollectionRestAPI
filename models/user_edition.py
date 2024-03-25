from db import db


class UserEditionModel(db.Model):
    __tablename__ = "user_edition"

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = "CASCADE"))
    edition_id = db.Column(db.Integer, db.ForeignKey("edition.id", ondelete = "CASCADE"))

    volumes_read = db.Column(db.Integer, nullable = False)
    wait_for_end = db.Column(db.Boolean, nullable = False)
    buy_priority = db.Column(db.Integer, nullable = False)
    notes = db.Column(db.String)
    private = db.Column(db.Boolean, nullable = False)
    
    user = db.relationship("UserModel", back_populates = "editions")
    edition = db.relationship("EditionModel", back_populates = "users")
    volumes = db.relationship("UserVolumeModel", back_populates = "user_edition", cascade = "all, delete")

    def __init__(self, user_id, edition_id, volumes_read = 0, wait_for_end = False, buy_priority = 0, notes = None, private = True):
        self.user_id = user_id
        self.edition_id = edition_id
        self.volumes_read = volumes_read
        self.wait_for_end = wait_for_end
        self.buy_priority = buy_priority
        self.notes = notes
        self.private = private

    def save_model_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_model_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()