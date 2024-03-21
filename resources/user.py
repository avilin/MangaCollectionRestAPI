from flask import request
from flask_restx import Resource, fields, Namespace

from repository.user import UserRepository


namespace = Namespace("user", description = "User related operations")

# Model required by flask_restx for expect
expected_model = namespace.model("UserModel", {
    "email": fields.String("Email"),
    "username": fields.String("Username"),
    "password": fields.String("Password")
})


@namespace.route("/<id>")
@namespace.param("id", "The model identifier")
class User(Resource):
    
    repository = UserRepository()

    def get(self, id):
        if (model := self.repository.find_by_id(id)) is None:
            return {"message": "Not found."}, 404
        
        return self.repository.dump_model(model), 200

    def delete(self, id):
        if (model := self.repository.find_by_id(id)) is None:
            return {"message": "Not found."}, 404
        
        self.repository.delete(model)
        return {"message": "Deleted successfully"}, 200


@namespace.route("/")
class UserList(Resource):

    repository = UserRepository()

    def get(self):
        models = self.repository.find_all()
        return self.repository.dump_models(models), 200

    @namespace.expect(expected_model)
    def post(self):
        model_json = request.get_json()
        model = self.repository.save_model_to_db_json(model_json)
        return self.repository.dump_model(model), 201