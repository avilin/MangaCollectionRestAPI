from typing import List

import db
from models.user_edition import UserEditionModel
from schemas.user_edition import UserEditionSchema
from repository.edition import EditionRepository
from repository.user_volume import UserVolumeRepository


class UserEditionRepository():

    model_schema = UserEditionSchema()
    models_schema = UserEditionSchema(many = True)

    edition_repository = EditionRepository()
    user_volume_repository = UserVolumeRepository()

    def save_model_to_db_json(self, model_json) -> UserEditionModel:
        return self.save_model_to_db_json_with_parent_id(model_json.get("user_id", None), model_json)

    def save_model_to_db_json_with_parent_id(self, user_id, model_json) -> UserEditionModel:
        if (edition_json := model_json.get("edition", None)) is not None:
            edition_model = self.edition_repository.save_model_to_db_json(edition_json)
        else:
            edition_model = self.edition_repository.find_by_id(model_json.get("edition_id", None))

        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_ids(user_id, edition_model.id)
        
        if model is None:
            model = UserEditionModel(
                user_id = user_id, 
                edition_id = edition_model.id,
            )

        if (volumes_read := model_json.get("volumes_read", None)) is not None:
            model.volumes_read = volumes_read

        if (volumes_have := model_json.get("volumes_have", None)) is not None:
            model.volumes_have = volumes_have

        if (wait_for_end := model_json.get("wait_for_end", None)) is not None:
            model.wait_for_end = wait_for_end

        if (buy_priority := model_json.get("buy_priority", None)) is not None:
            model.buy_priority = buy_priority

        model.notes = model_json.get("notes", None)

        if (private := model_json.get("private", None)) is not None:
            model.private = private
        
        db.save_model_to_db(model)

        if (user_volumes_json := model_json.get("user_volumes", None)) is not None:
            for user_volume_json in user_volumes_json:
                self.user_volume_repository.save_model_to_db_json_with_parent_id(model.id, user_volume_json)

        return model
    
    def find_all(cls) -> List[UserEditionModel]:
        return UserEditionModel.query.all()
        
    def find_by_id(cls, id) -> UserEditionModel:
        return UserEditionModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_ids(cls, user_id, edition_id) -> UserEditionModel:
        return UserEditionModel.query.filter_by(
            user_id = user_id, 
            edition_id = edition_id
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)