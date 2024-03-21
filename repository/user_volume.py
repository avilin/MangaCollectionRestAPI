from typing import List

import db
from models.user_volume import UserVolumeModel
from schemas.user_volume import UserVolumeSchema


class UserVolumeRepository():
    
    model_schema = UserVolumeSchema()
    models_schema = UserVolumeSchema(many = True)

    def save_model_to_db_json(self, model_json) -> UserVolumeModel:
        return self.save_model_to_db_json_with_parent_id(model_json.get("user_edition_id", None), model_json)

    def save_model_to_db_json_with_parent_id(self, user_edition_id, model_json) -> UserVolumeModel:
        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_user_edition_id_and_number(user_edition_id, model_json.get("number", None))
        
        if model is None:
            model = UserVolumeModel(
                user_edition_id = user_edition_id, 
                number = model_json.get("number", None),
                price = model_json.get("price", None)
            )

        db.save_model_to_db(model)

        return model
    
    def find_all(self) -> List[UserVolumeModel]:
        return UserVolumeModel.query.all()
        
    def find_by_id(self, id) -> UserVolumeModel:
        return UserVolumeModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_user_edition_id(self, user_edition_id) -> List[UserVolumeModel]:
        return UserVolumeModel.query.filter_by(
            user_edition_id = user_edition_id
        )
    
    def find_by_user_edition_id_and_number(self, user_edition_id, number) -> UserVolumeModel:
        return UserVolumeModel.query.filter_by(
            user_edition_id = user_edition_id, 
            number = number
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)