import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from flask_cors import CORS

import application.config as config
from application.security import user_datastore, security
from application.database import db



# Import all the controllers so they are loaded
from application.controllers import *

# Import all restfull controllers
from api.movie.moviesAPI import AllMovieAPI
from api.movie.moviesAPI import MovieAPI
from api.theater.theaterAPI import AllTheaterAPI
from api.theater.theaterAPI import TheaterAPI
from api.auth.loginAPI import LoginAPI
from api.auth.registerAPI import RegisterAPI
from api.ratings.movieRatingAPI import MovieRatingAPI
from api.ratings.theaterRatingAPI import TheaterRatingAPI
from api.theater_movie.TheaterMovieAPI import TheaterMovieAPI

from api.auth.loginAPI import RefreshTokenAPI


app = Flask(__name__)
app.config.from_object(config)
app.app_context().push()


# Flask CORS 
CORS(app, supports_credentials=True)


# Add CORS headers to every response
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    return response

@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response


# database initialize
db.init_app(app)

# API initilize
api = Api(app)
api.init_app(app)

# JWT initialization
JWTManager(app)


# Flask Security
security.init_app(app, user_datastore)

api.add_resource(AllMovieAPI, "/api/movie")
api.add_resource(MovieAPI, "/api/movie/<int:movie_id>")
api.add_resource(AllTheaterAPI, "/api/theater")
api.add_resource(TheaterAPI,"/api/theater/<int:theater_id>")
api.add_resource(LoginAPI, "/api/login")
api.add_resource(RegisterAPI, "/api/register")
api.add_resource(MovieRatingAPI,"/api/rating/movie/<int:user_id>/<int:movie_id>")
api.add_resource(TheaterRatingAPI,"/api/rating/theater/<int:user_id>/<int:theater_id>")
api.add_resource(TheaterMovieAPI, "/api/link_theater_movie/<int:theater_id>/<int:movie_id>")


api.add_resource(RefreshTokenAPI, "/api/token/refresh")

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8081)

