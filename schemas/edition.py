from ma import ma
from models.edition import EditionModel


class EditionSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = EditionModel
        include_fk = True
        load_instance = True

    series = ma.Nested("SeriesSchema", exclude = ("editions",))
    editorial = ma.Nested("EditorialSchema", exclude = ("editions",))
