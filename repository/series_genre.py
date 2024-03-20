from typing import List

import db
from models.series_genre import SeriesGenreModel
from schemas.series_genre import SeriesGenreSchema
from repository.genre import GenreRepository


class SeriesGenreRepository():

    model_schema = SeriesGenreSchema()
    models_schema = SeriesGenreSchema(many = True)

    genre_repository = GenreRepository()
    
    def save_model_to_db_json(self, model_json) -> SeriesGenreModel:
        return self.save_model_to_db_json_with_parent_id(model_json.get("series_id", None), model_json)

    def save_model_to_db_json_with_parent_id(self, series_id, model_json) -> SeriesGenreModel:
        if (genre_json := model_json.get("genre", None)) is not None:
            genre_model = self.genre_repository.save_model_to_db_json(genre_json)
        elif (genre_id := model_json.get("genre_id", None)) is not None:
            genre_model = self.genre_repository.find_by_id(genre_id)
        else:
            genre_model = self.genre_repository.save_model_to_db_json(model_json)

        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_ids(series_id, genre_model.id)
        
        if model == None:
            model = SeriesGenreModel(
                series_id = series_id, 
                genre_id = genre_model.id
            )

        db.save_model_to_db(model)

        return model

    def find_all(self) -> List[SeriesGenreModel]:
        return SeriesGenreModel.query.all()
        
    def find_by_id(self, id) -> SeriesGenreModel:
        return SeriesGenreModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_ids(self, series_id, genre_id) -> SeriesGenreModel:
        return SeriesGenreModel.query.filter_by(
            series_id = series_id, 
            genre_id = genre_id
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)

    def delete_unused_models(self):
        models = self.find_all()
        ids = list(map(lambda model: model.genre_id, models))
        self.genre_repository.delete_model_from_dbs_not_in_id_list(list(dict.fromkeys(ids)))
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)