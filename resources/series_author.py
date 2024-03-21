from flask import request
from flask_restx import Resource, fields, Namespace

from repository.series_author import SeriesAuthorRepository
from resources.decorators.authentication import token_required


namespace = Namespace("series_author", description = "SeriesAuthor related operations")

# Model required by flask_restx for expect
expected_model = namespace.model("SeriesAuthorModel", {
    "series_id": fields.Integer(min = 1),
    "author_id": fields.Integer(min = 1),
    "type": fields.String("Type")
})


@namespace.route("/<id>")
@namespace.param("id", "The model identifier")
class SeriesAuthor(Resource):
    
    repository = SeriesAuthorRepository()

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
class SeriesAuthorList(Resource):
    
    repository = SeriesAuthorRepository()

    def get(self):
        models = self.repository.find_all()
        return self.repository.dump_models(models), 200

    @namespace.expect(expected_model)
    def post(self):
        model_json = request.get_json()
        model = self.repository.save_model_to_db_json(model_json)
        return self.repository.dump_model(model), 201