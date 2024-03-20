from flask import Flask, Blueprint
from flask_restx import Api
from flask_cors import CORS

from resources.manga_updates import namespace as manga_updates_ns


app = Flask(__name__)
CORS(app, supports_credentials = True)
bluePrint = Blueprint("api", __name__, url_prefix="/api")
api = Api(bluePrint, doc="/doc", title="Manga Collection Application")
app.register_blueprint(bluePrint)

api.add_namespace(manga_updates_ns)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)