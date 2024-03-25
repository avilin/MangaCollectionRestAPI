from ma import ma
from models.user_edition import UserEditionModel


class UserEditionSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = UserEditionModel
        include_fk = True
        load_instance = True

    user = ma.Nested("UserSchema", only = ("id", "username",))
    edition = ma.Nested("EditionSchema", exclude = ("users",))
    volumes = ma.Nested("UserVolumeSchema", exclude = ("user_edition",), many = True)