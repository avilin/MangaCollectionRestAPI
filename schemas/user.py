from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = UserModel
        load_instance = True

    password = ma.String(load_only=True)

    series_list = ma.Nested("UserSeriesSchema", exclude = ("user_id", "user",), many = True)
    editions = ma.Nested("UserEditionSchema", exclude = ("user_id", "user",), many = True)