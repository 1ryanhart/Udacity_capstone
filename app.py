import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
      actors = []
      actors = Actor.query.all()

      if len(actors) == 0:
          abort(404)

      formatted_actors = [actor.format() for actor in actors]
      return jsonify(
      {
        'success': True,
        'actors': formatted_actors
      }), 200

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actors(payload):
      try:
          body = request.get_json()

          age = body.get('age', None)
          gender = body.get('gender', None)
          name = body.get('name', None)

          if not age or not gender or not name:
              abort(422)

          new_actor = Actor(age=age, gender=gender, name=name)
          new_actor.insert()

          return jsonify(
          {
            'success': True,
            'actor': new_actor.format()
          }), 200
      except:
          abort(422)

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, id):
      actor = Actor.query.filter(Actor.id==id).one_or_none()

      if actor is None:
          abort(404)

      actor.delete()

      return jsonify(
      {
        'success': True,
        'deleted': id
      }), 200

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actors(payload, id):
      actor = Actor.query.filter(Actor.id==id).one_or_none()
      if actor is None:
           abort(404)

      try:
          body = request.get_json()

          age = body.get('age', None)
          gender = body.get('gender', None)
          name = body.get('name', None)

          if not age or not gender or not name:
              abort(422)

          actor.age = age
          actor.gender = gender
          actor.name = name

          actor.update()

          return jsonify(
          {
            'success': True,
            'edited': actor.format()
          }), 200
      except:
          abort(422)

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
      movies = []
      movies = Movie.query.all()

      if len(movies) == 0:
          abort(404)

      formatted_movies = [movie.format() for movie in movies]
      return jsonify(
      {
        'success': True,
        'movies': formatted_movies
      })

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movies(payload):
      try:
          body = request.get_json()

          title = body.get('title', None)
          releaseDate = body.get('releaseDate', None)

          if not title or not releaseDate:
              abort(422)

          new_movie = Movie(title=title,releaseDate=releaseDate)
          new_movie.insert()

          return jsonify(
          {
            'success': True,
            'movie': new_movie.format()
          }), 200
      except:
          abort(422)

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(payload, id):
      movie = Movie.query.filter(Movie.id==id).one_or_none()

      if movie is None:
          abort(404)

      movie.delete()

      return jsonify(
      {
        'success': True,
        'deleted': id
      }), 200

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def patch_movies(payload, id):
      movie = Movie.query.filter(Movie.id==id).one_or_none()
      if movie is None:
          abort(404)

      try:
          body = request.get_json()

          title = body.get('title', None)
          releaseDate = body.get('releaseDate', None)

          if not title or not releaseDate:
              abort(422)

          movie.title = title
          movie.releaseDate = releaseDate
          movie.update()

          return jsonify(
          {
            'success': True,
            'edited': movie.format()
          }), 200
      except:
          abort(422)

# Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

  @app.errorhandler(404)
  def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

  @app.errorhandler(AuthError)
  def auth_error(error):
        return jsonify({
            "success":False,
            "error":error.status_code,
            "message":error.error
        }),error.status_code

  return app

app = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
