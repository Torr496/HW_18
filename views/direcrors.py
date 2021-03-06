
from flask_restx import Resource, Namespace
from models import Director, DirectorSchema

directors_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
from setup_db import db



@directors_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        if directors:
            return directors_schema.dump(directors), 200
        else:
            return "", 404



@directors_ns.route('/<int:nid>')
class DirectorView(Resource):
    def get(self, nid):
        genre = db.session.query(Director).get(nid)
        if genre:
            return director_schema.dump(genre), 200
        else:
            return "", 404


