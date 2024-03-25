from flask import request
from flask_restx import Resource, fields, Namespace

from repository.user_edition import UserEditionRepository
from resources.decorators.authentication import token_required


namespace = Namespace("user_edition", description = "UserEdition related operations")

# Model required by flask_restx for expect
expected_model = namespace.model("UserEditionModel", {
    "user_id": fields.Integer(min = 1),
    "edition_id": fields.Integer(min = 1),
    "volumes_read": fields.Integer(min = 0),
    "wait_for_end": fields.Boolean(default = False),
    "buy_priority": fields.Integer(min = 0),
    "notes": fields.String("Notes"),
    "private": fields.Boolean(default = True)
})


@namespace.route("/<id>")
@namespace.param("id", "The model identifier")
class UserEdition(Resource):
    
    repository = UserEditionRepository()

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
class UserEditionList(Resource):

    repository = UserEditionRepository()

    def get(self):
        models = self.repository.find_all()
        return self.repository.dump_models(models), 200

    @namespace.expect(expected_model)
    def post(self):
        model_json = request.get_json()
        model = self.repository.save_model_to_db_json(model_json)
        return self.repository.dump_model(model), 201