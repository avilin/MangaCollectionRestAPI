from ma import ma
from models.user_series import UserSeriesModel


class UserSeriesSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = UserSeriesModel
        include_fk = True
        load_instance = True

    user = ma.Nested("UserSchema", only = ("id", "username",))
    series = ma.Nested("BasicSeriesSchema")