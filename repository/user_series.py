from typing import List

import db
from models.user_series import UserSeriesModel
from schemas.user_series import UserSeriesSchema
from repository.series import SeriesRepository


class UserSeriesRepository():

    model_schema = UserSeriesSchema()
    models_schema = UserSeriesSchema(many = True)

    series_repository = SeriesRepository()

    def save_model_to_db_json(self, model_json) -> UserSeriesModel:
        return self.save_model_to_db_json_with_parent_id(model_json.get("user_id", None), model_json)

    def save_model_to_db_json_with_parent_id(self, user_id, model_json) -> UserSeriesModel:
        if (series_json := model_json.get("series", None)) is not None:
            series_model = self.series_repository.save_model_to_db_json(series_json)
        else:
            series_model = self.series_repository.find_by_id(model_json.get("series_id", None))
        
        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_ids(user_id, series_model.id)
        
        if model is None:
            model = UserSeriesModel(
                user_id = user_id, 
                series_id = series_model.id
            )

        model.rating = model_json.get("rating", None)
        model.review = model_json.get("review", None)
        model.timestamp = model_json.get("timestamp", None)

        if (private := model_json.get("private", None)) is not None:
            model.private = private
        
        db.save_model_to_db(model)

        return model
    
    def find_all(self) -> List[UserSeriesModel]:
        return UserSeriesModel.query.all()
        
    def find_by_id(self, id) -> UserSeriesModel:
        return UserSeriesModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_ids(self, user_id, series_id) -> UserSeriesModel:
        return UserSeriesModel.query.filter_by(
            user_id = user_id,
            series_id = series_id
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)