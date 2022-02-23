
from flask_restx import Resource, Namespace
from models import Director, DirectorSchema

directors_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)



@directors_ns.route("/")
class GenresView(Resource):
    def get(self):
        directors = Director.query.all()
        if directors:
            return directors_schema.dump(directors), 200
        else:
            return "", 404



@directors_ns.route('/<int:nid>')
class GenresView(Resource):
    def get(self, nid):
        genre = Director.query.get(nid)
        if genre:
            return director_schema.dump(genre), 200
        else:
            return "", 404


