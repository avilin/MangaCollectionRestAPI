from ma import ma
from models.series_genre import SeriesGenreModel


class SeriesGenreSchema(ma.SQLAlchemyAutoSchema):
    series = ma.Nested("SeriesSchema", exclude = ("genres",))
    genre = ma.Nested("GenreSchema", exclude = ("series_list",))

    class Meta:
        model = SeriesGenreModel
        include_fk = True
        load_instance = True