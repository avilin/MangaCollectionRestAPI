from flask import request
from flask_restx import Resource, fields, Namespace
import jwt

from config import config_json
from repository.user import UserRepository


namespace = Namespace("authentication", description = "Authentication related operations")

# Model required by flask_restx for expect
expected_model = namespace.model("UserModel", {
    "username": fields.String("Username"),
    "password": fields.String("Password")
})


@namespace.route("/login")
class Login(Resource):

    repository = UserRepository()

    @namespace.expect(expected_model)
    def post(self):
        model_json = request.get_json()
        if ((username := model_json.get("username", None)) is None 
            or (password := model_json.get("password", None)) is None):
            return {"message": "No login data"}, 401

        user = self.repository.find_by_username(username)
        if (user is None 
            or not user.check_password(password)):
            return {"message": "Wrong user data"}, 401
        
        token = jwt.encode({ "id": user.id, "username": user.username }, config_json["token_key"], "HS256")
        return { "token": token }, 201