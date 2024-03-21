from ma import ma
from models.user_volume import UserVolumeModel


class UserVolumeSchema(ma.SQLAlchemyAutoSchema):
    user_edition = ma.Nested("UserEditionSchema", exclude = ("user_id", "user",))

    class Meta:
        model = UserVolumeModel
        include_relationships = True
        load_instance = True