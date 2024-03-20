from ma import ma
from models.author import AuthorModel


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    series_list = ma.Nested("SeriesAuthorSchema", exclude = ("author_id", "author",), many = True)

    class Meta:
        model = AuthorModel
        include_relationships = True
        load_instance = True