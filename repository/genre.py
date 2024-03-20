from typing import List

import db
from models.genre import GenreModel
from schemas.genre import GenreSchema


class GenreRepository():
        
    model_schema = GenreSchema()
    models_schema = GenreSchema(many = True)

    def save_model_to_db_json(self, model_json) -> GenreModel:
        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_name(model_json.get("name", None))

        if model is None:
            model = GenreModel(
                name = model_json.get("name", None)
            )
        
        db.save_model_to_db(model)

        return model
    
    def find_all(self) -> List[GenreModel]:
        return GenreModel.query.all()
    
    def find_by_id(self, id) -> GenreModel:
        return GenreModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_name(self, name) -> GenreModel:
        return GenreModel.query.filter_by(
            name = name
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)

    def delete_model_from_dbs_not_in_id_list(self, ids):
        models = GenreModel.query.filter(
            GenreModel.id.notin_(ids)
        ).all()

        for model in models:
            db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)