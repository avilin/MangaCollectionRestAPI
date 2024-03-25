from ma import ma
from models.genre import GenreModel


class GenreSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = GenreModel
        load_instance = True

    series_list = ma.Nested("SeriesGenreSchema", exclude = ("genre_id", "genre",), many = True)