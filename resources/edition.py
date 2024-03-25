from flask import request
from flask_restx import Resource, fields, Namespace

from repository.edition import EditionRepository
from resources.decorators.authentication import token_required


namespace = Namespace("edition", description = "Edition related operations")

# Model required by flask_restx for expect
expected_model = namespace.model("EditionModel", {
    "editorial_id": fields.Integer(min = 1),
    "series_id": fields.Integer(min = 1),
    "format": fields.String("Format (Tankoubon, Omnibus, 3 in 1, Ultimate, Digital...)"),
    "volumes": fields.Integer(min = 0),
    "discontinued": fields.Boolean(default = False),
    "size": fields.String("Size"),
})


@namespace.route("/<id>")
@namespace.param("id", "The model identifier")
class Edition(Resource):
    
    repository = EditionRepository()

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
class EditionList(Resource):

    repository = EditionRepository()

    def get(self):
        models = self.repository.find_all()
        return self.repository.dump_models(models), 200

    @namespace.expect(expected_model)
    def post(self):
        model_json = request.get_json()
        model = self.repository.save_model_to_db_json(model_json)
        return self.repository.dump_model(model), 201