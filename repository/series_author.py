from typing import List

import db
from models.series_author import SeriesAuthorModel
from schemas.series_author import SeriesAuthorSchema
from repository.author import AuthorRepository


class SeriesAuthorRepository():

    model_schema = SeriesAuthorSchema()
    models_schema = SeriesAuthorSchema(many = True)

    author_repository = AuthorRepository()
    
    def save_model_to_db_json(self, model_json) -> SeriesAuthorModel:
        return self.save_model_to_db_json_with_parent_id(model_json.get("series_id", None), model_json)

    def save_model_to_db_json_with_parent_id(self, series_id, model_json) -> SeriesAuthorModel:
        if (author_json := model_json.get("author", None)) is not None:
            author_model = self.author_repository.save_model_to_db_json(author_json)
        elif (author_id := model_json.get("author_id", None)) is not None:
            author_model = self.author_repository.find_by_id(author_id)
        else:
            author_model = self.author_repository.save_model_to_db_json(model_json)

        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_ids_and_type(series_id, author_model.id, model_json.get("type", None))
        
        if model is not None:
            model.type = model_json.get("type", None)
        else:
            model = SeriesAuthorModel(
                series_id = series_id, 
                author_id = author_model.id,
                type = model_json.get("type", None)
            )

        db.save_model_to_db(model)

        return model

    def find_all(self) -> List[SeriesAuthorModel]:
        return SeriesAuthorModel.query.all()
        
    def find_by_id(self, id) -> SeriesAuthorModel:
        return SeriesAuthorModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_ids_and_type(self, series_id, author_id, type) -> SeriesAuthorModel:
        return SeriesAuthorModel.query.filter_by(
            series_id = series_id, 
            author_id = author_id,
            type = type,
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)

    def delete_unused_models(self):
        models = self.find_all()
        ids = list(map(lambda model: model.author_id, models))
        self.author_repository.delete_model_from_dbs_not_in_id_list(list(dict.fromkeys(ids)))
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)