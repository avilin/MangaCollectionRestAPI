from flask import request
from flask_restx import Resource, fields, Namespace

from repository.series import SeriesRepository
from resources.decorators.authentication import token_required

namespace = Namespace("series", description = "Series related operations")

#Model required by flask_restx for expect
expected_model = namespace.model("Series", {
    "id": fields.Integer(min = 1),
    "title": fields.String("Title"),
    "type": fields.String("Type"),
    "description": fields.String("Description"),
    "image_url": fields.String("ImageURL"),
    "status": fields.String("Status"),
    "completed": fields.Boolean(default = False),
    "anime_start": fields.String("Anime Start"),
    "anime_end": fields.String("Anime End"),
    "url": fields.String("MangaUpdates URL")
})


@namespace.route("/<id>")
@namespace.param("id", "The model identifier")
class Series(Resource):
    
    repository = SeriesRepository()

    def get(self, id):
        if (model := self.repository.find_by_id(id)) is None:
            return {"message": "Not found."}, 404
        
        return self.repository.dump_model(model), 200

    @token_required
    def delete(current_user, self, id):
        if (model := self.repository.find_by_id(id)) is None:
            return {"message": "Not found."}, 404
        
        self.repository.delete(model)
        return {"message": "Deleted successfully"}, 200


@namespace.route("/")
class SeriesList(Resource):

    repository = SeriesRepository()

    def get(self):
        models = self.repository.find_all()
        return self.repository.dump_models(models), 200

    @namespace.expect(expected_model)
    def post(self):
        model_json = request.get_json()
        model = self.repository.save_model_to_db_json(model_json)
        return self.repository.dump_model(model), 201