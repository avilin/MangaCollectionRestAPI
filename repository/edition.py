from typing import List

import db
from models.edition import EditionModel
from schemas.edition import EditionSchema
from repository.editorial import EditorialRepository


class EditionRepository():
    
    model_schema = EditionSchema()
    models_schema = EditionSchema(many = True)

    editorial_repository = EditorialRepository()

    def save_model_to_db_json(self, model_json) -> EditionModel:
        return self.save_model_to_db_json_with_parent_id(model_json.get("series_id", None), model_json)
    
    def save_model_to_db_json_with_parent_id(self, series_id, model_json) -> EditionModel:
        if (editorial_json := model_json.get("editorial", None)) is not None:
            editorial_model = self.editorial_repository.save_model_to_db_json(editorial_json)
        else:
            editorial_model = self.editorial_repository.find_by_id(model_json.get("editorial_id", None))

        model = self.find_by_id(model_json.get("id", None))

        if model is None:
            model = self.find_by_ids_and_format(series_id, editorial_model.id, model_json.get("volume_format", None))

        if model is None:
            model = EditionModel(
                editorial_id = editorial_model.id,
                series_id = series_id,
                volume_format = model_json.get("volume_format", None)
            )
        
        if (volumes := model_json.get("volumes", None)) is not None:
            model.volumes = volumes

        if (discontinued := model_json.get("discontinued", None)) is not None:
            model.discontinued = discontinued

        model.size = model_json.get("size", None)

        db.save_model_to_db(model)

        return model
        
    def find_all(self) -> List[EditionModel]:
        return EditionModel.query.all()
    
    def find_by_id(self, id) -> EditionModel:
        return EditionModel.query.filter_by(
            id = id
        ).first()
    
    def find_by_ids(self, series_id, editorial_id) -> List[EditionModel]:
        return EditionModel.query.filter_by(
            series_id = series_id, 
            editorial_id = editorial_id
        )
    
    def find_by_ids_and_format(self, series_id, editorial_id, volume_format) -> EditionModel:
        return EditionModel.query.filter_by(
            series_id = series_id, 
            editorial_id = editorial_id, 
            volume_format = volume_format
        ).first()
    
    def delete(self, model):
        db.delete_model_from_db(model)
    
    def dump_model(self, model):
        return self.model_schema.dump(model)
    
    def dump_models(self, models):
        return self.models_schema.dump(models)