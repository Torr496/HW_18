# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

# Пример

from flask import Flask
from flask_restx import Api
import json
from config import Config

from setup_db import db
from views.movies import movie_ns
from views.direcrors import directors_ns
from views.genres import genres_ns
from models import Director, Genre, Movie

# функция создания основного объекта app
def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(directors_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(genres_ns)
    create_data(app,db)

def create_data(app, db):
    with open('data.json', encoding='utf-8') as f:
        data = json.load(f)

    with app.app_context():
        db.create_all()

        for director in data["directors"]:
            with db.session.begin():
                db.session.add(Director(
                    id = director["pk"],
                    name = director["name"],
                ))

        for genre in data["genres"]:
            with db.session.begin():
                db.session.add(Genre(
                    id = genre["pk"],
                    name = genre["name"],
                ))

        for movie in data["movies"]:
            with db.session.begin():
                db.session.add(Movie(
                    id = movie["pk"],
                    title = movie["title"],
                    description=movie["description"],
                    trailer=movie["trailer"],
                    year=movie["year"],
                    rating=movie["rating"],
                    genre_id=movie["genre_id"],
                    director_id=movie["director_id"],
                ))

app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)



