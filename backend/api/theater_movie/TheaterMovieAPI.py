import json

from flask import request, jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from application.models import db,Movie,Theater, TheaterMovie,Dyanmic
from datetime import datetime

from flask_restful import Resource,reqparse,abort,fields,marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

theater_movie_post_args = reqparse.RequestParser()
theater_movie_post_args.add_argument('ticket_price', type=int, required = True, help='ticket price is required is required')
theater_movie_post_args.add_argument('timing', type=str,required=True,help="timming is required")

resource_fields = {
    'theater_id': fields.Integer,
    'theater_name' : fields.String,
    'theater_place': fields.String,
    'theater_location': fields.String,
    'theater_capacity': fields.Integer,
    'movie_id': fields.Integer,
    'movie_name' : fields.String,
    'movie_tag': fields.String,
    'movie_language': fields.String,
    'movie_duration': fields.String,
    'movie_description' : fields.String,
    'movie_image_path': fields.String,
    'ticket_price' : fields.Integer,
    'timing' : fields.DateTime,
}

class linkTheaterMovieAPI(Resource):
    @jwt_required()
    def post(self, theater_id,movie_id):
        args = theater_movie_post_args.parse_args()
        theater = Theater.query.filter_by(theater_id=theater_id).first()
        if not theater:
            return jsonify({'status':'failed', 'message':"theater not found"})
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        if not movie:
            return jsonify({'status':'failed', 'message':"theater not found"})
        input = TheaterMovie(theater=theater,movie=movie,ticket_price=args["ticket_price"], timing=args["timing"])
        db.session.add(input)
        db.session.commit()
        return jsonify({'status':'success','message': 'movie and theater linked'})


class allTheaterMovieAPI(Resource):
    @jwt_required()
    def get(resource):
        theatermovies = TheaterMovie.query.join(Movie,Theater).filter(TheaterMovie.movie_id == Movie.movie_id).filter(TheaterMovie.theater_id == Theater.theater_id).add_columns(TheaterMovie.theater_movie_id,Movie.movie_name,Theater.theater_name,TheaterMovie.timing,TheaterMovie.ticket_price)
        theatermovies_list = []
        for theatermovie in theatermovies:
            theatermovies_list.append({'id': theatermovie.theater_movie_id ,'theater_movie_id': theatermovie.theater_movie_id ,'theater_name': theatermovie.theater_name ,'movie_name': theatermovie.movie_name, "timing" : theatermovie.timing, "ticket_price": theatermovie.ticket_price})
        return theatermovies_list


class dltTheaterMovieAPI(Resource):
    @jwt_required()
    def delete(self, id):
        theatermovie = TheaterMovie.query.filter_by(theater_movie_id = id).first()
        if not theatermovie:
            return jsonify({'status':"failed",'message' : 'Theatermovie not exist!'})
        db.session.delete(theatermovie)
        db.session.commit()
        return jsonify({'status':"success",'message' : 'TheaterMovie has been deleted!'})


class MoviesAtTheaterAPI(Resource):
    @jwt_required()
    def get(resource):
        theaters = Theater.query.all()
        theaters_list = []
        for theater in theaters:
            theatermovies = TheaterMovie.query.join(Movie,Theater).filter(
            TheaterMovie.movie_id == Movie.movie_id).filter(
            TheaterMovie.theater_id == theater.theater_id).add_columns(
            TheaterMovie.theater_movie_id,Movie.movie_name, Movie.movie_tag,
            TheaterMovie.timing)
            movies_list = []
            for theatermovie in theatermovies:
                dynamic = Dyanmic.query.filter_by(theater_movie_id = theatermovie.theater_movie_id).first()
                if datetime.strptime(theatermovie.timing, '%Y-%m-%dT%H:%M') > datetime.now(): #2023-07-31T23:37
                    if dynamic.seats_left > 0:
                        movies_list.append({'theater_movie_id': theatermovie.theater_movie_id ,'theater_id' : theater.theater_id,
                                           'movie_name': theatermovie.movie_name,'movie_tag':theatermovie.movie_tag, "timing" : theatermovie.timing, "housefull": False})
                    else:
                        movies_list.append({'theater_movie_id': theatermovie.theater_movie_id ,'theater_id' : theater.theater_id,
                                           'movie_name': theatermovie.movie_name,'movie_tag':theatermovie.movie_tag, "timing" : theatermovie.timing, "housefull": True})
            theaters_list.append({'id':theater.theater_id,'theater_id':theater.theater_id,'theater_name':theater.theater_name, 'theater_place':theater.theater_place,
                            'theater_location':theater.theater_location,"movies":movies_list})
        
        return theaters_list
        



# {
#     "ticket_price" : 500,
#     "timing" : "time"
# }