import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Actor, Movie, Stageshow

ROWS_PER_PAGE = 10

def create_app(test_config=None):
  '''create and configure the app and CORS details'''
  
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  def get_error_message(error, default_text):
      try:
          # Return  error message
          return error.description['message']
      except:
          return default_text
  
  def paginate_results(request, selection):
    page = request.args.get('page', 1, type=int)  
    start =  (page - 1) * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE
    objects_formatted = [object_name.format() for object_name in selection]
    return objects_formatted[start:end]          


  @app.route('/')
  def welcome():      
      return "helloo world"

  @app.route('/actors', methods=['GET'])
  @requires_auth('view:actors')
  def get_actors(payload):
    selection = Actor.query.all()
    actors_paginated = paginate_results(request, selection)

    if len(actors_paginated) == 0:
      abort(404, {'message': 'no actors found in database.'})

    return jsonify({
      'success': True,
      'actors': actors_paginated
    })

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actor')
  def new_actor(payload):
 
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', 'Other')

    if not name:
      abort(422, {'message': 'no name provided.'})

    if not age:
      abort(422, {'message': 'no age provided.'})

    new_actor = (Actor(
          name = name, 
          age = age,
          gender = gender
          ))
    new_actor.insert()

    return jsonify({
      'success': True,
      'created': new_actor.id
    })

  @app.route('/actors/<actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def patch_actor(payload, actor_id):
    body = request.get_json()

    if not actor_id:
      abort(400, {'message': 'please check the input params'})

    actorupdateId = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if not actorupdateId:
      abort(404, {'message': 'Actor {} Details not found in database. Please check the ID'.format(actor_id)})

    name = body.get('name', actorupdateId.name)
    age = body.get('age', actorupdateId.age)
    gender = body.get('gender', actorupdateId.gender)

    actorupdateId.name = name
    actorupdateId.age = age
    actorupdateId.gender = gender

    actorupdateId.update()
    return jsonify({
      'success': True,
      'updated': actorupdateId.id,
      'actor' : [actorupdateId.format()]
    })

  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):

    if not actor_id:
      abort(400, {'message': 'please check the input params'})
  
    actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if not actor_to_delete:
        abort(404, {'message': 'Actor {} Details not found in database. Please check the ID'.format(actor_id)}) 
    actor_to_delete.delete()
    return jsonify({
      'success': True,
      'deleted': actor_id
    })

#movie releated endpoints

  @app.route('/movies', methods=['GET'])
  @requires_auth('view:movies')
  def get_movies(payload):

    selection = Movie.query.all()
    movies_paginated = paginate_results(request, selection)

    if len(movies_paginated) == 0:
      abort(404, {'message': 'no movies found in database. please add entries'})

    return jsonify({
      'success': True,
      'movies': movies_paginated
    })

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def insert_movies(payload):

    body = request.get_json()

    title = body.get('title', None)
    release_date = body.get('release_date', None)
    if not title:
      abort(422, {'message': 'no title provided.'})

    if not release_date:
      abort(422, {'message': 'no "release_date" provided.'})

    new_movie = (Movie(
          title = title, 
          release_date = release_date
          ))
    new_movie.insert()

    return jsonify({
      'success': True,
      'created': new_movie.id
    })

  @app.route('/movies/<movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def edit_movies(payload, movie_id):

    body = request.get_json()

    if not movie_id:
      abort(400, {'message': 'please check the input params'})

    movieupdateId = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if not movieupdateId:
      abort(404, {'message': 'Movie {} Details not found in database. Please check the ID.'.format(movie_id)})

    title = body.get('title', movieupdateId.title)
    release_date = body.get('release_date', movieupdateId.release_date)
    movieupdateId.title = title
    movieupdateId.release_date = release_date

    movieupdateId.update()

    return jsonify({
      'success': True,
      'edited': movieupdateId.id,
      'movie' : [movieupdateId.format()]
    })

  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movies(payload, movie_id):
    if not movie_id:
      abort(400, {'message': 'please check the input params'})

    movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if not movie_to_delete:
        abort(404, {'message': 'Movie {} Details not found in database. Please check the ID.'.format(movie_id)})
 
    movie_to_delete.delete()
    
    return jsonify({
      'success': True,
      'deleted': movie_id
    })

  # Common Error Handlers for 422, 400, 404  and Auth error

  @app.errorhandler(401)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 401,
                      "message": get_error_message(error,"unauthorized")
                      }), 401

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": get_error_message(error,"unprocessable")
                      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
                      "success": False, 
                      "error": 400,
                      "message": get_error_message(error, "bad request")
                      }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
      return jsonify({
                      "success": False, 
                      "error": 404,
                      "message": get_error_message(error, "resource not found")
                      }), 404

  @app.errorhandler(AuthError)
  def authentification_failed(AuthError): 
      return jsonify({
                      "success": False, 
                      "error": AuthError.status_code,
                      "message": AuthError.error['description']
                      }), AuthError.status_code


  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)