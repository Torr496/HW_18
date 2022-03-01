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
        director = request.args.get('director_id')
        genre = request.args.get('genre_id')
        year = request.args.get('year')
        t = db.session.query(Movie)
        if director is not None:
            t = t.filter(Movie.director_id == director)
        if genre is not None:
            t = t.filter(Movie.genre_id == genre)
        if year is not None:
            t = t.filter(Movie.year == year)
        all_movies = t.all()
        res = movies_schema.dump(all_movies)
        return res, 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        db.session.add(new_movie)
        db.session.commit()
        return "",201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = db.session.query(Movie).get(mid)
        if movie:
            return movie_schema.dump(movie), 200
        else:
            return "", 404

    def put(self, mid: int):
        movie = db.session.query(Movie).get(mid)
        if movie:
            req_json = request.json
            movie.title = req_json.get("title")
            movie.description = req_json.get("description")
            movie.trailer = req_json.get("trailer")
            movie.year = req_json.get("year")
            movie.rating = req_json.get("rating")
            movie.genre_id = req_json.get("genre_id")
            movie.director_id = req_json.get("director_id")
            db.session.add(movie)
            db.session.commit()
            return "", 200
        else:
            return "", 404

    def delete(self, mid: int):
        movie = db.session.query(Movie).get(mid)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return "", 200
        else:
            return "", 404
