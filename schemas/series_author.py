from ma import ma
from models.series_author import SeriesAuthorModel


class SeriesAuthorSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = SeriesAuthorModel
        include_fk = True
        load_instance = True

    series = ma.Nested("SeriesSchema", exclude = ("authors",))
    author = ma.Nested("AuthorSchema", exclude = ("series_list",))