# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки). сюда импортируются сервисы из пакета service

# Пример
from flask import request
from flask_restx import Resource, Namespace


movie_ns = Namespace('movies')
from models import Movie, MovieSchema
from setup_db import db


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MovieViews(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id and genre_id:
            movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id).all()
        elif director_id:
            movies = Movie.query.filter_by(director_id=director_id).all()
        elif genre_id:
            movies = Movie.query.filter_by(genre_id=genre_id).all()
        else:
            movies = Movie.query.all()
        if movies:
            return movies_schema.dump(movies), 200
        else:
            return "",404

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()
        return "",201


@movie_ns.route('/<int:nid>')
class MovieView(Resource):
    def get(self, nid):
        movie = Movie.query.get(nid)
        if movie:
            return movie_schema.dump(movie), 200
        else:
            return "", 404

    def put(self, mid: int):
        movie = Movie.query.get(mid)
        if movie:
            req_json = request.json
            movie.title = req_json.get("title")
            movie.description = req_json.get("description")
            movie.trailer = req_json.get("trailer")
            movie.year = req_json.get("year")
            movie.genre_id = req_json.get("genre_id")
            movie.director_id = req_json.get("director_id")
            db.session.add(movie)
            db.session.commit()
            return "", 200
        else:
            return "", 404

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return "", 200
        else:
            return "", 404
