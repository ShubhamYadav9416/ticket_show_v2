# Importing essential libraies--------------------------------
import os
import secrets
from flask import Flask, current_app
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from celery.schedules import crontab
from werkzeug.security import generate_password_hash
# importing configs and models---------------------------------
import application.config as config
from application.security import user_datastore, security
from application.data.database import db
from application.data.models import User
# Import internals for caching--------------------------------
from application.cache import cache
# Import Libraries for Celery---------------------------------
from application.jobs.workers import create_celery_app
from application.jobs import task


# ------------------------------------------------------------
# --------------Import all restful API Controllers------------
# ------------------------------------------------------------
from application.api.movie.moviesAPI import AllMovieAPI
from application.api.movie.moviesAPI import MovieAPI
from application.api.theater.theaterAPI import AllTheaterAPI
from application.api.theater.theaterAPI import TheaterAPI
from application.api.auth.loginAPI import LoginAPI
from application.api.auth.registerAPI import RegisterAPI
from application.api.auth.forgetAPI import ForgetAPI
from application.api.ratings.theaterRatingAPI import TheaterUserRatingAPI
from application.api.theater_movie.TheaterMovieAPI import linkTheaterMovieAPI
from application.api.theater_movie.TheaterMovieAPI import allTheaterMovieAPI
from application.api.theater_movie.TheaterMovieAPI import dltTheaterMovieAPI
from application.api.theater_movie.TheaterMovieAPI import MoviesAtTheaterAPI
from application.api.ratings.theaterRatingAPI import TheaterRating
from application.api.theater_movie.TheaterMovieAPI import TheaterMovieBooking
from application.api.ticket_booking.ticketBookingAPI import bookTicket
from application.api.ticket_booking.ticketBookingAPI import userBookedTicket
from application.api.search.searchAPI import Filters
from application.api.search.searchAPI import FilterByMovie
from application.api.search.searchAPI import FilterByTheater

from application.api.export_csv.exportCSVAPI import Export_CSV_API

from application.api.auth.loginAPI import RefreshTokenAPI


app = Flask(__name__)
app.config.from_object(config)
app.app_context().push()


# Flask CORS----------------------------------------
CORS(app, supports_credentials=True)


# Add CORS headers to every response-----------------
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


# database initialize---------------------------------
db.init_app(app)

# Creating a admin user in database when it is a created
def create_initial_user():
    if User.query.filter_by(user_mail="admin@gmail.com").first() is None:
        admin_user = User(user_mail="admin@gmail.com" , password= generate_password_hash('1234'), admin = True)
        admin_user.fs_uniquifier = secrets.token_hex(16)
        db.session.add(admin_user)
        db.session.commit()


# API initilize---------------------------------------
api = Api(app)
api.init_app(app)

# JWT initialization-----------------------------------
JWTManager(app)


# Flask Caching-----------------------------------------
cache.init_app(app)

# Celery ----------------------------------------------
cel_app = create_celery_app(app)

cel_app.conf.update(
    broker = app.config['CELERY_BROKER_URL'],
    backend = app.config['CELERY_RESULT_BACKEND'],
    timezone = 'Asia/Calcutta',
    enable_utc = False
)


# celery beats tasks scheduling-------------------------
@cel_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(
    #     10.0, 
    #     task.send_mail_monthly.s(), 
    #     name='Reminder every 10 seconds.'
    # )
    sender.add_periodic_task(
        crontab(minute=0, hour=19, day_of_month='*'),
        task.send_mail_daily.s(),
        name = 'Daily reminder everyday @7PM via mail.'
    )

    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        task.send_mail_monthly.s(),
        name = 'Monthly Engagement Report @1st of every month via mail.'
    )


# Flask Security--------------------------------------
security.init_app(app, user_datastore)


# giving paths for APIS--------------------------------
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
api.add_resource(Filters,'/api/search/filters')
api.add_resource(FilterByMovie,'/api/search/movie/<int:id>')
api.add_resource(FilterByTheater, '/api/search/theater/<int:id>')

api.add_resource(Export_CSV_API, '/api/export_csv/<int:id>')

api.add_resource(RefreshTokenAPI, "/api/token/refresh")


with app.app_context():
    db.create_all()
    create_initial_user()

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0',port=8081,debug=True)

