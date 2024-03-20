from ma import ma
from models.genre import GenreModel


class GenreSchema(ma.SQLAlchemyAutoSchema):
    series_list = ma.Nested("SeriesGenreSchema", exclude = ("genre_id", "genre",), many = True)

    class Meta:
        model = GenreModel
        include_relationships = True
        load_instance = True