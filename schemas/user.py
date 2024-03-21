from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    password = ma.String(load_only=True)

    series_list = ma.Nested("UserSeriesSchema", exclude = ("user_id", "user",), many = True)

    class Meta:
        model = UserModel
        include_relationships = True
        load_instance = True