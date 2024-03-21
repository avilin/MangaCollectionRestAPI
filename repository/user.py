from typing import List

import db
from models.user import UserModel
from schemas.user import UserSchema
from repository.user_series import UserSeriesRepository


class UserRepository():

    model_schema = UserSchema()
    models_schema = UserSchema(many = True)

    user_series_repository = UserSeriesRepository()

    def save_model_to_db_json(self, model_json) -> UserModel:
        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_email(model_json.get("email", None))

        if model is None:
            model = self.find_by_username(model_json.get("username", None))

        if model:
            model.email = model_json.get("email", None)
            model.username = model_json.get("username", None)
        else:
            model = UserModel(
                email = model_json.get("email", None),
                username = model_json.get("username", None),
                password = model_json.get("password", None)
            )
        
        db.save_model_to_db(model)

        if (user_series_list_json := model_json.get("user_series_list", None)) is not None:
            for user_series_json in user_series_list_json:
                self.user_series_repository.save_model_to_db_json_with_parent_id(model.id, user_series_json)

        return model
    
    
    def save_super_admin(self, model_json):
        model = self.find_by_username(model_json.get("username", None))

        if model:
            model.email = model_json.get("email", None)
            model.username = model_json.get("username", None)
            model.update_password(model_json.get("password", None))
            model.rights = "SUPERADMIN"
        else:
            model = UserModel(
                email = model_json.get("email", None),
                username = model_json.get("username", None),
                password = model_json.get("password", None),
                rights = "SUPERADMIN"
            )
        
        db.save_model_to_db(model)
    
    def change_user_rights(self, model_json):
        model = self.find_by_id(model_json.get("id", None))

        if (rights := model_json.get("rights", None)) is not None:
            model.rights = rights
    
    def change_password(self, model_json):
        model = self.find_by_id(model_json.get("id", None))

        if ((password := model_json.get("password", None)) is not None 
            and (last_password := model_json.get("last_password", None)) 
            and model.check_password(last_password)):
            model.update_password(password)
    
    def find_all(self) -> List[UserModel]:
        return UserModel.query.all()
    
    def find_by_id(self, id) -> UserModel:
        return UserModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_email(self, email) -> UserModel:
        return UserModel.query.filter_by(
            email = email
        ).first()
    
    def find_by_username(self, username) -> UserModel:
        return UserModel.query.filter_by(
            username = username
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)