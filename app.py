import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import setup_db,  Movie, Actor, setup_migrations
from auth.auth import AuthError, requires_auth
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

from datetime import datetime

def create_app(db_name="", test_config=None):

    app = Flask(__name__)

    db_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

    if db_path:
        setup_db(app,db_path)
    else: 
        setup_db(app)
    
    setup_migrations(app)

    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    # APP home route
    @app.route('/')
    def home_url_check():
        return jsonify({"success": True, 
                        "message": "Hello! This is  our Home URL page"})

    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def get_all_movies(payload):
        try:
            movies_query = Movie.query.order_by(Movie.id).all()
            movies = [movie.serialized_movie() for movie in movies_query]


        except Exception as e:
            print("Error while getting all Movies", e)
        
        if len(movies) == 0:
            print("Movies Database is empty")
            abort(404)

        return jsonify({
            "success": True,
            "movies": movies
        })

    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(payload):
        req_body = request.get_json()
        name = req_body.get("name", None)
        release_date = req_body.get("release_date", None)

        if  name is None or release_date is None:
            print("Release_date or Name cannot be empty")
            abort(400)
        else:
            try:
                movie_data = Movie(name=name,release_date=release_date)
                movie_data.insert()
            except Exception as e:
                print("Error occured while during INSERT", e)
                abort(422)
        return jsonify({'success': True, 'movie': movie_data.serialized_movie()})

    @app.route('/movie/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            print("No movie found to be deleted", movie)
            abort(404)
        try:
            # Delete the selected Movie record 
            movie.delete()
        except Exception as e:
            print("Error occured while Deleting the movie", e)
            abort(422)

        return jsonify({'success': True, 'id': movie_id})


    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(payload, movie_id):
        movie_tbu = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie_tbu is None:
            print("No movie found for updation with movie id: ", movie_id)
            abort(404)
        try:
            movie_data = request.get_json()
            name = movie_data.get("name", None)
            release_date = movie_data.get("release_date", None)

            if name is not None:
                movie_tbu.name = name
            if release_date is not None:
                movie_tbu.release_date = release_date
            
            movie_tbu.update()
        
        except Exception as e:
            print("Error occured while during UPDATE", e)
            abort(422)
        return jsonify({"success": True,
                        "movie": movie_tbu.serialized_movie()})

    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def get_all_actors(payload):
        try:
            actors_query = Actor.query.order_by(Actor.id).all()
            actors = [actor.serialized_actor() for actor in actors_query]
        except Exception as e:
            print("Error while getting all Actors", e)
        
        if len(actors) == 0:
            print("Actors Database is empty")
            abort(404)

        return jsonify({
            "success": True,
            "actors": actors
        })

    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(payload):
        req_body = request.get_json()
        name = req_body.get("name", None)
        age  = req_body.get("age", None)
        gender = req_body.get("gender", None)

        if  name is None or age is None or gender is None:
            print("Name or Age or Gender cannot be Empty")
            abort(400)
        else:
            try:
                actor_data = Actor(name=name,age=age,gender=gender)
                actor_data.insert()
            except Exception as e:
                print("Error occured while during INSERT", e)
                abort(422)
        return jsonify({'success': True, 'actor': actor_data.serialized_actor()})

    @app.route('/actor/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            print("No actor found to be deleted", actor)
            abort(404)
        try:
            # Delete the selected Actor record 
            actor.delete()
        except Exception as e:
            print("Error occured while Deleting the actor", e)
            abort(422)

        return jsonify({'success': True, 'id': actor_id})


    @app.route('/actor/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(payload, actor_id):
        actor_tbu = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor_tbu is None:
            print("No actor found for updation with Actor ID: ", actor_id)
            abort(404)
        try:
            actor_data = request.get_json()
            name = actor_data.get("name", None)
            age = actor_data.get("age", None)
            gender = actor_data.get("gender", None)

            if name is not None:
                actor_tbu.name = name
            if age is not None:
                actor_tbu.age = age
            if gender is not None:
                actor_tbu.gender = gender

            actor_tbu.update()
        
        except Exception as e:
            print("Error occured while during UPDATE", e)
            abort(422)
        return jsonify({"success": True,
                        "actor": actor_tbu.serialized_actor()})

    return app

app = create_app()

if __name__ == '__main__':
    app.run()