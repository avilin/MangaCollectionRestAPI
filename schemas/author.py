from ma import ma
from models.author import AuthorModel


class AuthorSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = AuthorModel
        load_instance = True

    series_list = ma.Nested("SeriesAuthorSchema", exclude = ("author_id", "author",), many = True)