from ma import ma
from models.series_genre import SeriesGenreModel


class SeriesGenreSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = SeriesGenreModel
        include_fk = True
        load_instance = True

    series = ma.Nested("SeriesSchema", exclude = ("genres",))
    genre = ma.Nested("GenreSchema", exclude = ("series_list",))