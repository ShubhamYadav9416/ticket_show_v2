import json

from flask import request, jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from application.models import db,Movie,Theater, TheaterMovie
from datetime import datetime

theater_movie_post_args = reqparse.RequestParser()
theater_movie_post_args.add_argument('ticket_price', type=int, required = True, help='ticket price is required is required')
theater_movie_post_args.add_argument('timing', type=str,required=True,help="timming is required")

resource_fields = {
    'theater_id': fields.Integer,
    'theater_name' : fields.String,
    'theater_place': fields.String,
    'theater_location': fields.String,
    'theater_capacity': fields.Integer,
    'theater_image_path' : fields.String,
    'movie_id': fields.Integer,
    'movie_name' : fields.String,
    'movie_tag': fields.String,
    'movie_language': fields.String,
    'movie_duration': fields.Integer,
    'movie_description' : fields.String,
    'movie_image_path': fields.String,
    'ticket_price' : fields.Integer,
    'timing' : fields.DateTime,
}

class TheaterMovieAPI(Resource):
    def post(self, theater_id,movie_id):
        args = theater_movie_post_args.parse_args()
        theater = Theater.query.filter_by(theater_id=theater_id).first()
        if not theater:
            abort(404, message="theater not found")
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        if not movie:
            abort(404,message="movie not found")
        input = TheaterMovie(theater=theater,movie=movie,ticket_price=args["ticket_price"],timing= datetime.now()) #timing=args["timing"])
        db.session.add(input)
        db.session.commit()
        return jsonify({'message': 'movie and theater linked'})

# class TheatersWithMovieAPI(Resource):
#     def get(self,movie_id):
#         theatersmovies=TheaterMovie.query.filter_by(movie_id=movie_id).all()
#         list={}
#         for theatermovie in theatersmovies:
#             list[]



# {
#     "ticket_price" : 500,
#     "timing" : "time"
# }