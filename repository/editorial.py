from typing import List

import db
from models.editorial import EditorialModel
from schemas.editorial import EditorialSchema


class EditorialRepository():

    model_schema = EditorialSchema()
    models_schema = EditorialSchema(many = True)
        
    def save_model_to_db_json(self, model_json) -> EditorialModel:
        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_name(model_json.get("name", None))

        if model is None:
            model = EditorialModel(
                name = model_json.get("name", None),
                language = model_json.get("language", None)
            )
        
        db.save_model_to_db(model)

        return model
    
    def find_all(self) -> List[EditorialModel]:
        return EditorialModel.query.all()
    
    def find_by_id(self, id) -> EditorialModel:
        return EditorialModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_name(self, name) -> EditorialModel:
        return EditorialModel.query.filter_by(
            name = name
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)