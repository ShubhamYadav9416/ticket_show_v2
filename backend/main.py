import os
from flask import Flask, current_app
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.security import generate_password_hash


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
from api.auth.forgetAPI import ForgetAPI
from api.ratings.theaterRatingAPI import TheaterUserRatingAPI
from api.theater_movie.TheaterMovieAPI import linkTheaterMovieAPI
from api.theater_movie.TheaterMovieAPI import allTheaterMovieAPI
from api.theater_movie.TheaterMovieAPI import dltTheaterMovieAPI
from api.theater_movie.TheaterMovieAPI import MoviesAtTheaterAPI
from api.ratings.theaterRatingAPI import TheaterRating
from api.theater_movie.TheaterMovieAPI import TheaterMovieBooking
from api.ticket_booking.ticketBookingAPI import bookTicket
from api.ticket_booking.ticketBookingAPI import userBookedTicket

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
api.add_resource(ForgetAPI,"/api/forget_pass")
api.add_resource(TheaterUserRatingAPI,"/api/user/rating/theater/<int:theater_id>")
api.add_resource(TheaterRating, "/api/rating/theater/<int:theater_id>")
api.add_resource(linkTheaterMovieAPI, "/api/link_theater_movie/<int:theater_id>/<int:movie_id>")
api.add_resource(allTheaterMovieAPI,"/api/theater_movie")
api.add_resource(dltTheaterMovieAPI,"/api/dlt/theater_movie/<int:id>")
api.add_resource(MoviesAtTheaterAPI,"/api/movies_at_theater/home")
api.add_resource(TheaterMovieBooking,"/api/theater_movie/booking/<int:id>")
api.add_resource(bookTicket,"/api/book_ticket/<int:theater_movie_id>")
api.add_resource(userBookedTicket,"/api/user/bookings")

api.add_resource(RefreshTokenAPI, "/api/token/refresh")

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0',port=8081)

