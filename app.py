from flask import Flask, Blueprint, jsonify
from flask_restx import Api
from flask_cors import CORS
from marshmallow import ValidationError
from ma import ma
from db import db

from config import config_json
from repository.user import UserRepository

from resources.series import namespace as series_ns
from resources.author import namespace as author_ns
from resources.series_author import namespace as series_author_ns
from resources.genre import namespace as genre_ns
from resources.series_genre import namespace as series_genre_ns
from resources.editorial import namespace as editorial_ns
from resources.edition import namespace as edition_ns
from resources.user import namespace as user_ns
from resources.user_series import namespace as user_series_ns
from resources.user_edition import namespace as user_edition_ns
from resources.user_volume import namespace as user_volume_ns

from resources.manga_updates import namespace as manga_updates_ns

from resources.authentication import namespace as authentication_ns


app = Flask(__name__)
CORS(app, supports_credentials = True)
bluePrint = Blueprint("api", __name__, url_prefix="/api")
api = Api(bluePrint, doc="/doc", title="Manga Collection Application")
app.register_blueprint(bluePrint)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///manga_collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

api.add_namespace(series_ns)
api.add_namespace(author_ns)
api.add_namespace(series_author_ns)
api.add_namespace(genre_ns)
api.add_namespace(series_genre_ns)
api.add_namespace(editorial_ns)
api.add_namespace(edition_ns)
api.add_namespace(user_ns)
api.add_namespace(user_series_ns)
api.add_namespace(user_edition_ns)
api.add_namespace(user_volume_ns)

api.add_namespace(manga_updates_ns)

api.add_namespace(authentication_ns)

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()
    UserRepository().save_super_admin(config_json["superadmin"])

@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)