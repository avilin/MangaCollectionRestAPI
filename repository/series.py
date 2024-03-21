from typing import List

import db
from models.series import SeriesModel
from schemas.series import SeriesSchema
from repository.series_author import SeriesAuthorRepository
from repository.series_genre import SeriesGenreRepository
from repository.edition import EditionRepository


class SeriesRepository():
    
    model_schema = SeriesSchema()
    models_schema = SeriesSchema(many = True)

    series_author_repository = SeriesAuthorRepository()
    series_genre_repository = SeriesGenreRepository()
    edition_repository = EditionRepository()

    def save_model_to_db_json(self, model_json) -> SeriesModel:

        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_title(model_json.get("title", None))

        if model:
            model.title = model_json.get("title", None)
        else:
            model = SeriesModel(
                id = model_json.get("id", None),
                title = model_json.get("title", None)
            )

        model.type = model_json.get("type", None)
        model.description = model_json.get("description", None)
        model.image_url = model_json.get("image_url", None)
        model.status = model_json.get("status", None)
        model.completed = model_json.get("completed", None)
        model.anime_start = model_json.get("anime_start", None)
        model.anime_end = model_json.get("anime_end", None)
        model.url = model_json.get("url", None)
        
        db.save_model_to_db(model)

        if (authors_json := model_json.get("authors", None)) is not None:
            for author_json in authors_json:
                self.series_author_repository.save_model_to_db_json_with_parent_id(model.id, author_json)

        if (genres_json := model_json.get("genres", None)) is not None:
            for genre_json in genres_json:
                self.series_genre_repository.save_model_to_db_json_with_parent_id(model.id, genre_json)

        if (editions_json := model_json.get("editions", None)) is not None:
            for edition_json in editions_json:
                self.edition_repository.save_model_to_db_json_with_parent_id(model.id, edition_json)

        return model
    
    def find_all(self) -> List[SeriesModel]:
        return SeriesModel.query.all()
    
    def find_by_id(self, id) -> SeriesModel:
        return SeriesModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_title(self, title) -> SeriesModel:
        return SeriesModel.query.filter_by(
            title = title
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)