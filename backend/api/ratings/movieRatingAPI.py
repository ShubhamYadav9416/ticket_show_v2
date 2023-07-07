import json

from flask import request, jsonify
from flask_restful import Resource,reqparse,abort,fields,marshal_with
from application.models import db,Movie,User, MovieRating

rating_post_args = reqparse.RequestParser()
rating_post_args.add_argument('rating', type=int, required = True, help='rating is required')

class MovieRatingAPI(Resource):
    def get(self,user_id,movie_id):
        movierating = MovieRating.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        if not movierating:
            abort(404,message='User does\'nt rate this movie')
        return jsonify({'rating':movierating.rating})
    
    def post(self,user_id,movie_id):
        args = rating_post_args.parse_args()
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        user = User.query.filter_by(user_id=user_id).first()
        if not movie:
            abort(404, message = 'movie not found')
        if not user:
            abort(404, message = 'user not found')
        input = MovieRating(users = user, movie=movie, rating = args['rating'])
        db.session.add(input)
        db.session.commit()
        return  {'status' : 'success', 'message': 'Rated!!'}



