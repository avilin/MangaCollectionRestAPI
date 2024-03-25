from ma import ma
from models.user_volume import UserVolumeModel


class UserVolumeSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = UserVolumeModel
        load_instance = True