from ma import ma
from models.user_series import UserSeriesModel


class UserSeriesSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested("UserSchema", only = ("id", "username",))
    series = ma.Nested("SeriesSchema", exclude = ("users",))

    class Meta:
        model = UserSeriesModel
        include_fk = True
        load_instance = True