from ma import ma
from models.edition import EditionModel


class EditionSchema(ma.SQLAlchemyAutoSchema):
    series = ma.Nested("SeriesSchema", exclude = ("editions",))
    editorial = ma.Nested("EditorialSchema", exclude = ("editions",))
    users = ma.Nested("UserEditionSchema", many = True, exclude = ("edition",))

    class Meta:
        model = EditionModel
        include_fk = True
        load_instance = True