from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from models import MovieSchema, DirectorSchema, GenreSchema, Movie, Director, Genre

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
db = SQLAlchemy(app)


api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    """
    Вывод все
    """
    def get(self):
        all_movies = db.session.query(Movie).all()

        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()

            return "", 201


@movie_ns.route('/<int:bid>')
class MoviesView(Resource):
    def get(self, bid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == bid).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, bid: int):
        movie = db.session.query(Movie).get(bid)
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

        return "", 204

    def patch(self, bid: int):
        movie = db.session.query(Movie).get(bid)
        req_json = request.json

        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "director_id" in req_json:
            movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, bid: int):
        movie = db.session.query(Movie).get(bid)

        db.session.delete(movie)
        db.session.commit()

        return "", 204


@director_ns.route('/')
class DirectorsView(Resource):
    """
    Вывод все
    """
    def get(self):
        all_directors = db.session.query(Director).all()

        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)

        with db.session.begin():
            db.session.add(new_director)
            db.session.commit()

            return "", 201


@director_ns.route('/<int:bid>')
class DirectorsView(Resource):
    def get(self, bid: int):
        try:
            director = db.session.query(Director).filter(Director.id == bid).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, bid: int):
        director = db.session.query(Director).get(bid)
        req_json = request.json

        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()

        return "", 204

    def patch(self, bid: int):
        director = db.session.query(Director).get(bid)
        req_json = request.json

        if "name" in req_json:
            director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()

        return "", 204

    def delete(self, bid: int):
        director = db.session.query(Director).get(bid)

        db.session.delete(director)
        db.session.commit()

        return "", 204


@genre_ns.route('/')
class GenresView(Resource):
    """
    Вывод все
    """
    def get(self):
        all_genres = db.session.query(Genre).all()

        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)

        with db.session.begin():
            db.session.add(new_genre)
            db.session.commit()

            return "", 201


@genre_ns.route('/<int:bid>')
class GenresView(Resource):
    def get(self, bid: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == bid).one()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, bid: int):
        genre = db.session.query(Genre).get(bid)
        req_json = request.json

        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()

        return "", 204

    def patch(self, bid: int):
        genre = db.session.query(Genre).get(bid)
        req_json = request.json

        if "name" in req_json:
            genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()

        return "", 204

    def delete(self, bid: int):
        genre = db.session.query(Genre).get(bid)

        db.session.delete(genre)
        db.session.commit()

        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
