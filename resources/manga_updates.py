from flask import request
from flask_restx import Resource, fields, Namespace
import requests
import json


namespace = Namespace("manga_updates", description = "Manga Updates API related operations")

#Model required by flask_restx for expect
search_expected_model = namespace.model("Search", {
    "title": fields.String("Title")
})


@namespace.route("/series/<id>")
@namespace.param("id", "The series identifier")
class MangaUpdatesSeries(Resource):

    def get(self, id):
        url = "https://api.mangaupdates.com/v1/series/" + id
        response = requests.get(url)        
        return response.json()


@namespace.route("/search/")
class MangaUpdatesSearch(Resource):

    @namespace.expect(search_expected_model)
    def post(self):
        search_json = request.get_json()
        url = "https://api.mangaupdates.com/v1/series/search"
        body = json.dumps({"search": search_json["title"], 
                           "per_page": 50, 
                           "type": ["Artbook", "Manga", "Manhua", "Manhwa", "Novel"], 
                           "exclude_genre": ["Doujinshi", "Hentai"], 
                           "orderby": "score"})
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, data=body, verify=False)
        
        return response.json()