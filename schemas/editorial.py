from ma import ma
from models.editorial import EditorialModel


class EditorialSchema(ma.SQLAlchemyAutoSchema):
    editions = ma.Nested("EditionSchema", exclude = ("editorial_id", "editorial",), many = True)

    class Meta:
        model = EditorialModel
        include_relationships = True
        load_instance = True