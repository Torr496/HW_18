
from flask_restx import Resource, Namespace
from models import Genre, GenreSchema

genres_ns = Namespace('genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

from setup_db import db

@genres_ns.route("/")
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).query.all()
        if genres:
            return genres_schema.dump(genres), 200
        else:
            return "", 404



@genres_ns.route('/<int:nid>')
class GenreView(Resource):
    def get(self, nid):
        genre = db.session.query(Genre).query.get(nid)
        if genre:
            return genre_schema.dump(genre), 200
        else:
            return "", 404


