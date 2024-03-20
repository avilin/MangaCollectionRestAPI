from ma import ma
from models.series import SeriesModel


class SeriesSchema(ma.SQLAlchemyAutoSchema):
    genres = ma.Nested("SeriesGenreSchema", exclude = ("genre_id", "series_id", "series",), many = True)
    authors = ma.Nested("SeriesAuthorSchema", exclude = ("author_id", "series_id", "series",), many = True)

    class Meta:
        model = SeriesModel
        include_relationships = True
        load_instance = True