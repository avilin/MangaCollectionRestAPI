from typing import List

import db
from models.author import AuthorModel
from schemas.author import AuthorSchema


class AuthorRepository():
    
    model_schema = AuthorSchema()
    models_schema = AuthorSchema(many = True)

    def save_model_to_db_json(self, model_json) -> AuthorModel:
        model = self.find_by_id(model_json.get("id", None))

        print(model)
        if model is None:
            model = self.find_by_name(model_json.get("name", None))

        print(model)
        if model is None:
            model = AuthorModel(
                id = model_json.get("id", None),
                name = model_json.get("name", None)
            )
        
        db.save_model_to_db(model)

        return model
        
    def find_all(self) -> List[AuthorModel]:
        return AuthorModel.query.all()
    
    def find_by_id(self, id) -> AuthorModel:
        return AuthorModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_name(self, name) -> AuthorModel:
        return AuthorModel.query.filter_by(
            name = name
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)

    def delete_model_from_dbs_not_in_id_list(self, ids):
        models = AuthorModel.query.filter(
            AuthorModel.id.notin_(ids)
        ).all()

        for model in models:
            db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)