from ma import ma
from models.editorial import EditorialModel


class EditorialSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = EditorialModel
        load_instance = True

    editions = ma.Nested("EditionSchema", exclude = ("editorial_id", "editorial",), many = True)