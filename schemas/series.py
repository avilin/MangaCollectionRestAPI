from ma import ma
from models.series import SeriesModel


class SeriesSchema(ma.SQLAlchemyAutoSchema):
    genres = ma.Nested("SeriesGenreSchema", exclude = ("genre_id", "series_id", "series",), many = True)
    authors = ma.Nested("SeriesAuthorSchema", exclude = ("author_id", "series_id", "series",), many = True)
    editions = ma.Nested("EditionSchema", exclude = ("series_id", "series",), many = True)
    users = ma.Nested("UserSeriesSchema", exclude = ("series_id", "series",), many = True)

    class Meta:
        model = SeriesModel
        include_relationships = True
        load_instance = True


class BasicSeriesSchema(ma.SQLAlchemySchema):

    class Meta:
        model = SeriesModel
        load_instance = True

    id = ma.auto_field()
    title = ma.auto_field()
    image_url = ma.auto_field()
    avg_rating = ma.Method("get_average_ratings")

    def get_average_ratings(self, obj):
        ratings = list(map(lambda userSeries: userSeries.rating, obj.users))
        return sum(ratings) / len(ratings)